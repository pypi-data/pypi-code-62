import json
from datetime import datetime, timedelta
from typing import Union

from google import auth  # type: ignore
from google.auth.transport._http_client import Request
from google.cloud.tasks_v2 import CloudTasksClient  # type: ignore
from google.cloud.tasks_v2.types import Task  # type: ignore
from google.cloud.tasks_v2.types import Duration
from google.protobuf import timestamp_pb2

__version__ = "0.0.3"


class TaskQueue:
    def __init__(
        self,
        cloud_tasks_client: CloudTasksClient = None,
        *,
        project_id: str = None,
        location_id: str = "us-central1",
        queue_id: str = None,
    ):
        self.client = cloud_tasks_client or CloudTasksClient()
        self.project_id = project_id or auth.default()[1]
        self.credentials, self.project_id = auth.default()
        if self.credentials.service_account_email == "default":
            self.credentials.refresh(Request())
        self.location_id = location_id
        self.queue_id = queue_id

    def create_http_task(
        self,
        url: str,
        task=None,
        *,
        location_id: str = None,
        queue_id: str = None,
        task_name: str = None,
        method: str = "POST",
        in_seconds: Union[int, float] = None,
        deadline: int = None,
        audience: str = None,
    ) -> Task:
        if not url.startswith(("http", "https")):
            raise ValueError("url must starts with http or https")
        queue_id = queue_id or self.queue_id
        if queue_id is None:
            raise ValueError("queue_id must be set")
        location_id = location_id or self.location_id
        if location_id is None:
            raise ValueError("location_id must be set")
        if in_seconds and (in_seconds > 1800 or in_seconds <= 0):
            raise ValueError("in_seconds must <= 1800 and > 0")
        if deadline and (deadline > 1800 or deadline < 15):
            raise ValueError("deadline must <= 1800 and >= 15")

        http_request = {
            "http_method": method,
            "url": url,
            "headers": [("Content-Type", "application/json")],
            "oidc_token": {
                "service_account_email": self.credentials.service_account_email
            },
        }
        if audience is not None:
            http_request["oidc_token"]["audience"] = audience
        if task is not None:
            http_request["body"] = json.dumps(task).encode()
        task = {"http_request": http_request}

        if task_name is not None:
            task["name"] = self.client.task_path(
                self.project_id, location_id, queue_id, task_name
            )
        if in_seconds is not None:
            dt = datetime.utcnow() + timedelta(seconds=in_seconds)
            schedule_time = timestamp_pb2.Timestamp()
            schedule_time.FromDatetime(dt)
            task["schedule_time"] = schedule_time

        if deadline is not None:
            task["dispatch_deadline"] = Duration(seconds=deadline)

        queue_path = self.client.queue_path(self.project_id, location_id, queue_id)
        return self.client.create_task(queue_path, task)

    def create_appengine_task(
        self,
        relative_uri: str,
        task=None,
        *,
        location_id: str = None,
        queue_id: str = None,
        service: str = None,
        task_name: str = None,
        method: str = "POST",
        in_seconds: Union[int, float] = None,
        deadline: int = None,
        audience: str = None,
    ) -> Task:
        if not relative_uri.startswith("/"):
            raise ValueError("relative_uri must starts with /")
        queue_id = queue_id or self.queue_id
        if queue_id is None:
            raise ValueError("queue_id must be set")
        location_id = location_id or self.location_id
        if location_id is None:
            raise ValueError("location_id must be set")
        if in_seconds and (in_seconds > 3600 or in_seconds <= 0):
            raise ValueError("in_seconds must <= 3600 and > 0")
        if deadline and (deadline > 3600 or deadline < 15):
            raise ValueError("deadline must <= 3600 and >= 15")

        app_engine_http_request = {
            "http_method": method,
            "app_engine_routing": {"service": service},
            "relative_uri": relative_uri,
            "headers": [("Content-Type", "application/json")],
            "oidc_token": {
                "service_account_email": self.credentials.service_account_email
            },
        }
        if audience is not None:
            app_engine_http_request["oidc_token"]["audience"] = audience
        if task is not None:
            app_engine_http_request["body"] = json.dumps(task).encode()
        task = {"app_engine_http_request": app_engine_http_request}

        if task_name is not None:
            task["name"] = self.client.task_path(
                self.project_id, location_id, queue_id, task_name
            )
        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            dt = datetime.utcnow() + timedelta(seconds=in_seconds)

            # Create Timestamp protobuf.
            schedule_time = timestamp_pb2.Timestamp()
            schedule_time.FromDatetime(dt)

            # Add the schedule_time to the tasks.
            task["schedule_time"] = schedule_time

        if deadline is not None:
            task["dispatch_deadline"] = Duration(seconds=deadline)

        queue_path = self.client.queue_path(self.project_id, location_id, queue_id)
        return self.client.create_task(queue_path, task)
