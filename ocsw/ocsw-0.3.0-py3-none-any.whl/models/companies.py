from datetime import datetime

from .blueprints import BlueprintCollection
from .resource import BaseCollection, BaseModel


class Company(BaseModel):
    """
        "id"
        "adminGroupId"
        "avCompanyId"
        "creationDate"
        "creatorId"
        "displayName"
        "name"
        "usersGroupId"
        "zuoraAccountId"
        "zuoraAccountNumber"
    """

    @property
    def blueprints(self):
        return BlueprintCollection(client=self.client, parent=self)

    @property
    def creation_date(self):
        """The creation date of the Company."""
        timestamp = self.attrs.get("creationDate")
        return datetime.fromtimestamp(timestamp / 1000.0)

    @property
    def display_name(self):
        """The description of the Company."""
        return self.attrs.get("displayName")

    @property
    def name(self):
        """The name of the Company."""
        return self.attrs.get("name")


class CompanyCollection(BaseCollection):
    """Local Actions(Edge Actions) collection."""

    model = Company

    async def get(self, action_id):
        return self.prepare_model(
            await self.client.api.inspect_company(action_id)
        )

    async def list(self):
        resp = await self.client.api.companies()
        return [self.prepare_model(item) for item in resp.get("body")]
