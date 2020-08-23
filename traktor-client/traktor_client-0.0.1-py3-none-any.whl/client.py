from typing import Optional, List


from traktor_client import errors
from traktor_client.http import HttpClient
from traktor_client.models import (
    Auth,
    Project,
    ProjectCreateRequest,
    ProjectUpdateRequest,
    Task,
    TaskCreateRequest,
    TaskUpdateRequest,
    Timer,
    Report,
)


class Client:
    def __init__(self, url, token):
        self.url = url
        self.http = HttpClient(
            url=f"{self.url.rstrip('/')}/api/v0", token=token or ""
        )

    # Auth
    def login(self, username: str, password: str) -> str:
        """Obtain authentication token.

        Args:
            username: Traktor username.
            password: Traktor password.

        Returns:
            str: Authentication token.
        """
        response = self.http.post(
            "/auth/token/", data=Auth(username=username, password=password)
        )
        return response["token"]

    # Projects

    def project_list(self) -> List[Project]:
        return [Project(**p) for p in self.http.get("/projects/")]

    def project_get(self, project_id: str) -> Project:
        return Project(**self.http.get(f"/projects/{project_id}/"))

    @errors.handler
    def project_create(self, name: str, color: str = "#000000") -> Project:
        return Project(
            **self.http.post(
                "/projects/", data=ProjectCreateRequest(name=name, color=color)
            )
        )

    @errors.handler
    def project_update(
        self,
        project_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Project:
        return Project(
            **self.http.patch(
                f"/projects/{project_id}/",
                data=ProjectUpdateRequest(name=name, color=color),
            )
        )

    def project_delete(self, project_id: str):
        return self.http.delete(f"/projects/{project_id}/")

    # Tasks

    def task_list(self, project_id: str) -> List[Task]:
        return [
            Task(**t) for t in self.http.get(f"/projects/{project_id}/tasks/")
        ]

    def task_get(self, project_id: str, task_id: str) -> Task:
        return Task(
            **self.http.get(f"/projects/{project_id}/tasks/{task_id}/")
        )

    @errors.handler
    def task_create(
        self, project_id: str, name: str, color: str = "#000000", default=False
    ) -> Task:

        return Task(
            **self.http.post(
                f"/projects/{project_id}/tasks/",
                data=TaskCreateRequest(
                    name=name, color=color, default=default
                ),
            )
        )

    @errors.handler
    def task_update(
        self,
        project_id: str,
        task_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        default: Optional[bool] = None,
    ) -> Task:

        return Task(
            **self.http.patch(
                f"/projects/{project_id}/tasks/{task_id}/",
                data=TaskUpdateRequest(
                    name=name, color=color, default=default
                ),
            )
        )

    def task_delete(self, project_id: str, task_id: str):
        return self.http.delete(f"/projects/{project_id}/tasks/{task_id}/")

    # Timer

    def timer_start(
        self, project_id: str, task_id: Optional[str] = None
    ) -> Timer:
        url = (
            f"/timer/start/{project_id}/"
            if task_id is None
            else f"/timer/start/{project_id}/{task_id}/"
        )
        return Timer(**self.http.post(url))

    def timer_stop(self) -> Timer:
        return Timer(**self.http.post("/timer/stop/"))

    def timer_status(self) -> Timer:
        return Timer(**self.http.get("/timer/status/"))

    def timer_today(self) -> List[Report]:
        return [Report(**r) for r in self.http.get("/timer/today/")]

    def timer_report(self, days: int = 0) -> List[Report]:
        return [
            Report(**r)
            for r in self.http.get("/timer/report/", params={days: days})
        ]
