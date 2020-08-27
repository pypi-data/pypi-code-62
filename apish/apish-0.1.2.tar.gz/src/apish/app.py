from starlette.requests import Request
from fastapi import FastAPI
from apish.metadata import Metadata
from apish.routes import RouteGenerator, Namespace, Resource


ns = Namespace(["Generic"])


@ns.route("/metadata")
class Info(Resource):
    async def get(self, request: Request) -> Metadata:
        """Show API metadata"""
        return request.app.metadata


@ns.route("/health")
class Health(Resource):
    async def get(self):
        """Show health status"""
        return {"status": "ok"}


class Application(FastAPI):
    def __init__(self, root: str, metadata: Metadata, **kwargs):
        self.root = root
        self.metadata = metadata
        super().__init__(
            root_path="",
            title=metadata.title,
            version=metadata.version.api,
            openapi_url=f"{root}/openapi.json",
            docs_url=f"{root}/docs",
            redoc_url=None,
            **kwargs,
        )
        self.add(ns)

    def add(self, route_generator: RouteGenerator) -> None:
        for route in route_generator.routes(prefix=self.root):
            self.routes.append(route)

    def openapi(self):
        openapi = super().openapi()
        if self.metadata.contact:
            openapi["info"]["contact"] = self.metadata.contact.dict(exclude_unset=True)
        if self.metadata.api_id:
            openapi["info"]["x-api-id"] = self.metadata.api_id
        if self.metadata.audience:
            openapi["info"]["x-audience"] = self.metadata.audience
        return openapi
