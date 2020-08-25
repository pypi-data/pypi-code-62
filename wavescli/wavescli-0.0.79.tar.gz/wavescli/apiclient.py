import yaml
import json
from stl_sdk.waves import WavesClient


class ApiClient(object):

    def __init__(self, url, key):
        if not url:
            raise RuntimeError('WAVES_URL environment variable not set')

        if not key:
            raise RuntimeError('API_KEY environment variable not set')

        self.client = WavesClient(url, key)
        self._workflow = None

    def workflow(self, identifier):
        self._workflow = self.client.get_workflow(identifier)
        self._execution = None
        return self

    def get_inputs(self):
        if self._execution:
            return self._execution['inputs']
        elif self._workflow:
            self._inputs = {}
            for item in self._workflow['definition']['inputs']:
                self._inputs[item['name']] = '' if item.get('required') else None
                if item.get('default'):
                    self._inputs[item['name']] = item.get('default')
            return self._inputs
        return {}

    def execution(self, identifier=None):
        if not identifier:
            self._execution = None
            self._inputs = None
            return self

        self._execution = self.client.get_execution(identifier)
        self._inputs = self._execution['inputs']
        self._workflow = self._execution['workflow']
        return self

    def create(self, inputs=None, description=None):
        if self._execution and not inputs:
            return self.run(
                workflow_identifier=self._workflow['identifier'],
                inputs=self._inputs,
            )

        elif self._workflow and inputs and not description:
            return self.run(
                workflow_identifier=self._workflow['identifier'],
                inputs=inputs,
                description=None
            )
        else:
            return self.run(
                workflow_identifier=self._workflow['identifier'],
                inputs=inputs,
                description=description
            )
        self._results = None
        return {
            "message": "Nothing to do",
        }

    def register_businesstask(self, btask_content):
        btask = self._parse_yaml_to_json(btask_content)
        return self.client.create_businesstask(btask)

    def publish_businesstask(self, btask_content):
        btask = json.loads(self._parse_yaml_to_json(btask_content))
        print(type(btask))
        print(btask)
        identifier = '{}@{}'.format(btask.get('name'), btask.get('version', 'latest'))
        return self.client.publish_businesstask(identifier)

    def create_workflow(self, workflow_content):
        workflow = self._parse_yaml_to_json(workflow_content)
        return self.client.create_workflow(workflow)

    def run(self, workflow_identifier, inputs, description):
        self._results = self.client.create_execution(workflow_identifier, inputs, description)
        return self._results

    def list_executions(self, term=None, status=None, sort_by='-created_at', page=1, size=200):
        """
        Lists all executions that have not been deleted
        """
        self._results = self.client.list_executions(term, status, sort_by, page, size)
        return self._results

    def list_workers(self):
        return self.client.list_workers()

    def _parse_yaml_to_json(self, content):
        try:
            parsed = yaml.safe_load(content)
            result = json.dumps(parsed)
        except yaml.YAMLError:
            result = content
        
        return result
