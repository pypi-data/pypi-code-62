import datetime
import re
import time
import traceback
from datetime import datetime
from typing import List

from common.logger import get_logger
from tabulate import tabulate
from common.objects import Events, Resources, Stacks, Event, Resource, Outputs, Output


class StackStatus:
    COMPLETE = ["CREATE_COMPLETE", "UPDATE_COMPLETE", "DELETE_COMPLETE"]
    IN_PROGRESS = [
        "CREATE_IN_PROGRESS",
        "DELETE_IN_PROGRESS",
        "UPDATE_IN_PROGRESS",
        "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
        "ROLLBACK_IN_PROGRESS"
    ]
    FAILED = [
        "DELETE_FAILED",
        "CREATE_FAILED",
        "ROLLBACK_IN_PROGRESS",
        "ROLLBACK_FAILED",
        "ROLLBACK_COMPLETE",
        "UPDATE_ROLLBACK_IN_PROGRESS",
        "UPDATE_ROLLBACK_FAILED",
        "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
        "UPDATE_ROLLBACK_COMPLETE",
    ]
    CREATE_FAIL_REASON = [
        "CREATE_FAILED",
        "ROLLBACK_IN_PROGRESS"
    ]


class Capabilities:
    IAM = "CAPABILITY_IAM"
    NAMED_IAM = "CAPABILITY_NAMED_IAM"
    AUTO_EXPAND = "CAPABILITY_AUTO_EXPAND"
    ALL = [IAM, NAMED_IAM, AUTO_EXPAND]


class IterStack(type):
    def __iter__(cls):
        return iter(cls._allStacks)


class Stack(metaclass=IterStack):
    _allStacks = []

    def __init__(self, test_name, region, test_data, template_path, logger, aws_client, stack_name=None, stack_id=None):
        self.logger = logger if logger else get_logger(__name__)

        # Test Details
        self.test_name = test_name
        self.template_path = template_path
        self.test_data = test_data
        self.parameters = test_data["parameters"]
        self.region = region

        # Stack Details
        self.parameters = self._generate_parameters(self.parameters)
        self.stack_name = stack_name if stack_name else re.sub('[^A-Za-z0-9]+', '', test_name + "_" + self.region)
        self.aws_client = aws_client
        self.cf_client_object = self.aws_client.cf_client_instance(self.region)

        # Stack Resources after Stack creation is done
        self.events = Events()
        self.resources = Resources()
        self.children = Stacks()
        self.outputs = Outputs()

        # Additional Stack Properties
        self.stack_id = stack_id
        self.change_set_id: str = ""
        self.created_parameters: List[dict] = []
        self.creation_time: datetime = datetime.fromtimestamp(0)
        self.status: str = ""
        self.status_reason: str = ""
        self.capabilities: List[str] = []
        self.tags: List[dict] = []
        self.parent_id: str = ""
        self.root_id: str = ""

    def deploy_template(self):
        deployment_error = []
        # Add Stacks to iter object when you are creating the Stack.
        self._allStacks.append(self)
        ll_stack_exists = False
        try:
            # -- Check if this stack name already exists
            existing_stack = self.aws_client.describe_stacks(self.cf_client_object, self.stack_name)
            if existing_stack:
                ll_stack_exists = True
                self.stack_id = existing_stack["StackId"]
        except Exception as e:
            ll_stack_exists = False

        try:
            # -- If the stack already exists then delete it first
            if ll_stack_exists:
                self.logger.info("As Stack %s Already Exist, Deleting the Stack First." % self.stack_name)
                self.delete_stack()

            # -- Create Stack
            response = self.aws_client.create_stack(self.cf_client_object, self.stack_name, self.template_path,
                                                    self.parameters, Capabilities.ALL)
            self.stack_id = response["StackId"]
            current_status = self._check_status()
            self.refresh()
            self._print_stack_events(self.events)
            if current_status in StackStatus.FAILED:
                self.logger.info("Stack %s Creation Failed with Status as %s." % (self.stack_name, current_status))
                status = "FAIL"
                deployment_error = [{"Resources": self.stack_name, "Message": self._get_failure_reasons()}]
            else:
                self.logger.info("Stack %s Creation Complete." % self.stack_name)
                status = "PASS"
        except Exception as e:
            # traceback.print_exc()
            status = "FAIL"
            deployment_error = [{"Resources": self.stack_name, "Message": str(e)}]
        return status, deployment_error

    def _get_failure_reasons(self):
        deployment_error = []
        for event in self.events:
            if event.status in StackStatus.CREATE_FAIL_REASON:
                deployment_error.append({"FailedStackName": self.stack_name,
                                         "Resource": event.logical_id,
                                         "Message": event.status_reason, })
                children = self.children.filter({"stack_id": event.physical_id})
                if children:
                    deployment_error.extend(children[0]._get_failure_reasons())
        return deployment_error

    def refresh(self, properties: bool = True, events: bool = True, resources: bool = True, children: bool = True):
        if properties:
            self._set_stack_properties()
        if events:
            self._fetch_events()
        if resources:
            self._fetch_resources()
        if children:
            self._fetch_children()

    @staticmethod
    def _generate_parameters(parameters):
        stack_parameters = []
        if parameters:
            for parameter_name, parameter_value in parameters.items():
                stack_parameters.append({"ParameterKey": parameter_name, "ParameterValue": parameter_value})
        return stack_parameters

    def _check_status(self):
        current_stack = self.aws_client.describe_stacks(self.cf_client_object, self.stack_id)
        current_status = None
        if current_stack:
            current_status = current_stack["StackStatus"]
            for ln_loop in range(1, 9999):
                self.logger.debug("Inside the loop with count as %s" % ln_loop)
                if current_status in StackStatus.IN_PROGRESS:
                    time.sleep(30)
                    try:
                        current_stack = self.aws_client.describe_stacks(self.cf_client_object, self.stack_id)
                    except Exception as e:
                        current_status = "DELETE_COMPLETE"
                        break
                    if current_stack["StackStatus"] != current_status:
                        current_status = current_stack["StackStatus"]
                else:
                    break
                self.logger.info("Stack -> %s, Current Status -> %s.", self.stack_name, current_status)
        return current_status

    def delete_stack(self):
        current_status = self._check_status()
        self.logger.debug("Starting Stack %s deletion with current status as %s" % (self.stack_name, current_status))
        for i in range(1, 10):
            if current_status == "DELETE_FAILED":
                self.refresh(properties=False, events=False, children=False)
                failed_resources = self.resources.filter({"status": "DELETE_FAILED"})
                failed_resources_ids = [failed_resource.logical_id for failed_resource in failed_resources]
                self.logger.info("Retain Resources %s and delete the stack %s again." % (
                    ', '.join(failed_resources_ids), self.stack_name))
                self.aws_client.delete_stack(self.cf_client_object, self.stack_id, failed_resources_ids)
            elif current_status not in StackStatus.IN_PROGRESS:
                child_stack_ids = self._get_child_stack_ids()
                for child_stack_id in child_stack_ids:
                    self.aws_client.delete_stack(self.cf_client_object, child_stack_id)
            current_status = self._check_status()

            if current_status != "DELETE_COMPLETE":
                continue
            else:
                self.logger.info("Complete Stack %s deletion with current status as DELETE_COMPLETE" % self.stack_name)
                break
        return current_status

    def _get_child_stack_ids(self):
        stack_ids = set()
        stack_ids.add(self.stack_id)
        for child_stack in self.children:
            stack_ids.update(child_stack._get_child_stack_ids())
        return stack_ids

    def _set_stack_properties(self):
        current_stack = self.aws_client.describe_stacks(self.cf_client_object, self.stack_id)
        if current_stack:
            self.change_set_id = current_stack["ChangeSetId"] if "ChangeSetId" in current_stack else None
            self.created_parameters = current_stack["Parameters"] if "Parameters" in current_stack else None
            self.creation_time = current_stack["CreationTime"] if "CreationTime" in current_stack else None
            self.status = current_stack["StackStatus"] if "StackStatus" in current_stack else None
            self.status_reason = current_stack["StackStatusReason"] if "StackStatusReason" in current_stack else None
            self.capabilities = current_stack["Capabilities"] if "Capabilities" in current_stack else None
            if "Outputs" in current_stack:
                for output in current_stack["Outputs"]:
                    self.outputs.append(Output(output))
            self.tags = current_stack["Tags"] if "Tags" in current_stack else None
            self.parent_id = current_stack["ParentId"] if "ParentId" in current_stack else None
            self.root_id = current_stack["RootId"] if "RootId" in current_stack else None
            self.logger.debug("Successfully Fetched Stack Properties " + self.stack_name)

    def _fetch_resources(self):
        resources = Resources()
        response = self.aws_client.list_stack_resources(self.cf_client_object, self.stack_id)
        if response:
            for resource in response:
                resources.append(Resource(resource))
        self.resources = resources
        self.logger.debug("Successfully Fetched Stack Resources " + self.stack_name)

    def _fetch_events(self):
        events = Events()
        response = self.aws_client.list_stack_events(self.cf_client_object, self.stack_id)
        if response:
            for event in response:
                events.append(Event(event))
        self.events = events
        self.logger.debug("Successfully Fetched Stack Events " + self.stack_name)

    # Add Children Stack Properties, Outputs, Resources
    def _fetch_children(self):
        for resource in self.resources:
            if resource.physical_id and "arn:aws:cloudformation" in resource.physical_id \
                    and "WaitCondition" not in resource.type:
                child_stack = self.aws_client.describe_stacks(self.cf_client_object, resource.physical_id)
                if child_stack:
                    stack_obj = Stack(test_name=self.test_name, region=self.region, test_data=self.test_data,
                                      template_path=self.template_path, logger=self.logger,
                                      stack_name=child_stack["StackName"], stack_id=child_stack["StackId"],
                                      aws_client=self.aws_client)
                    stack_obj.refresh()
                    self.children.append(stack_obj)
        self.logger.debug("Successfully Fetched Stack Children " + self.stack_name)

    def _print_stack_events(self, events):
        self.logger.info(
            "********** Events -> Stack Name -> %s, Region -> %s **********" % (self.stack_name, self.region))
        headers = ['Timestamp', 'Resource Name', 'Resource Type', 'Resource Status', 'Resource Status Reason']
        rows = []
        for event in events:
            rows.append([event.timestamp, event.logical_id, event.type, event.status, event.status_reason])

        self.logger.info("\n" + tabulate(rows, headers=headers, tablefmt='orgtbl') + "\n")

        self.logger.info("************************** Events End **************************")
