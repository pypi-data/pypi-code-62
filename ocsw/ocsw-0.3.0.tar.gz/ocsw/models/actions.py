from .resource import BaseCollection, BaseModel


"""
    "id"
    "companyId"
    "creationDate"
    "creatorId":
    "description"
    "disabled"
    "js"
    "lastEditDate"
    "lastEditorId"
    "source"
    "version"
"""


class Action(BaseModel):
    @property
    def description(self):
        """The description of the Action."""
        return self.attrs.get("description")

    def disabled(self):
        """The disabled of the Action."""
        return self.attrs.get("disabled")

    def js(self):
        """The js of the Action."""
        return self.attrs.get("js")

    def source(self):
        """The source of the Action."""
        return self.attrs.get("source")

    def version(self):
        """The version of the Action."""
        return self.attrs.get("version")


class LocalAction(Action):
    pass


class CloudAction(Action):
    pass


class EdgeActionCollection(BaseCollection):
    """Local Actions(Edge Actions) collection."""

    model = LocalAction

    def get(self, action_id, company_name=None, version_number=None):
        return self.prepare_model(
            self.client.api.inspect_edge_action(
                action_id,
                company_name=company_name,
                version_number=version_number,
            )
        )

    def list(self, company_name=None):
        resp = self.client.api.edge_actions(company_name=company_name)
        return [self.prepare_model(item) for item in resp]


class CloudActionCollection(BaseCollection):
    """Cloud Actions collection."""

    model = CloudAction

    def get(self, action_id, company_name=None, version_number=None):
        return self.prepare_model(
            self.client.api.inspect_action(
                action_id,
                company_name=company_name,
                version_number=version_number,
            )
        )

    def list(self, company_name=None):
        resp = self.client.api.actions(company_name=company_name)
        return [self.prepare_model(item) for item in resp]
