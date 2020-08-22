import asyncio
from datetime import datetime

from .actions import EdgeActionCollection, LocalAction
from .resource import BaseCollection, BaseModel


"""
    "id":
    "companyId":
    "creationDate":
    "creatorId": 
    "displayName":
    "edgePackage":
    "lastEditDate":
    "lastEditorId":
    "localActions": {
      "l5ef5b4cefebea2b69e87c6df": {
        "version":
      },
    },
    "observations": 
    "state":
    "version":

"""


class Blueprint(BaseModel):
    @property
    def creation_date(self):
        """The creation date of the Company."""
        timestamp = self.attrs.get("creationDate")
        return datetime.fromtimestamp(timestamp / 1000.0)

    @property
    def last_edit_date(self):
        """The last changed date of the Company."""
        timestamp = self.attrs.get("lastEditDate")
        return datetime.fromtimestamp(timestamp / 1000.0)

    @property
    def display_name(self):
        """The description of the Company."""
        return self.attrs.get("displayName")

    @property
    def version(self):
        """The version of the Action."""
        return self.attrs.get("version")

    @property
    def local_actions(self):
        return self.attrs.get("localActions", [])

    @property
    def companyId(self):
        return self.attrs.get("companyId")


class BlueprintCollection(BaseCollection):
    """Local Actions(Edge Actions) collection."""

    model = Blueprint

    async def get(self, blueprint_id, version_number=None):
        resp = await self.client.api.inspect_blueprint(
            blueprint_id,
            company_name=self.parent.name,
            version_number=version_number,
            refs=1,
        )

        map_refs = [("localAction", EdgeActionCollection, "localActions")]

        body = resp.get("body")
        references = resp.get("head", {}).get("references", {})
        for ref_key, model, target_key in map_refs:
            items = references.get(ref_key, {}).values()
            model(client=self.client, parent=self)

            body[target_key] = model(client=self.client, parent=self)
        return self.prepare_model(body)

    async def list(self, company_name=None):
        resp = await self.client.api.blueprints(
            company_name=self.parent.name, fields=["id"]
        )
        futures = [self.get(item["id"]) for item in resp.get("body")]
        return await asyncio.gather(*futures)
