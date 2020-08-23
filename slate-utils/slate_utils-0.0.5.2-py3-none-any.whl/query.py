import requests

from slate_utils.common import pkv
from slate_utils.session import SlateSession


class QueryTool:
    """Class for interacting with the Query backend. Mainly used to remove query runs and individual ids from query
    runs en masse."""

    def __init__(self, session: SlateSession):
        self.hostname = session.headers.get("Origin")
        self.session = session

    def remove_run_id(
        self, query: str, run: str, id: str, id2: str = ""
    ) -> requests.Response:
        """Remove an id from a query run.

        Parameters
        ----------
        query : str (guid)
            The guid of the query
        run : str (guid)
            The guid of the query run (`[query.run.id].[run]`).
        id : str (guid)
            The id (`[query.run.id].[id]`) of the record to be removed.
        id2 : str (guid)
            The id2 (`[query.run.id].[id2]`) of the record to be removed.
        """
        url = f"{self.hostname}/manage/query/run?cmd=results&id={query}&run={run}"
        response = self.session.post(
            url, data={"run_id": id, "run_id2": id2, "cmd": "remove"}
        )
        response.raise_for_status()
        assert "parent.FW.Dialog.Unload" in response.text
        return response

    def remove_run(self, query: str, run: str) -> requests.Response:
        """Remove a query run.

        Parameters
        ----------
        query : str (guid)
            The guid of the query (`[query.run].[query]`).
        id : str (guid)
            The id of the run to be removed (`[query.run].[id]`)
        """
        url = f"{self.hostname}/manage/query/run?cmd=edit&id={query}&run={run}"
        response = self.session.post(url, data={"cmd": "delete"})
        response.raise_for_status()
        assert "parent.FW.Dialog.Unload" in response.text
        return response

    def edit_notes(self, query: str, html: str) -> requests.Response:
        """Replace the notes attribute of the given query with the specified html.

        Parameters
        ----------
        query : str (guid)
            The id of the query to edit.
        html : str (html)
            The html string of the notes. Slate is looking for html>head[title]+body.
        """
        url = f"{self.hostname}/manage/query/query?cmd=notes&id={query}"
        response = self.session.post(url, data={"cmd": "save", "notes": html})
        response.raise_for_status()
        return response

    def run_to_browser(self, query: str) -> requests.Response:
        """Run the specified query to browser.

        Parameters
        ----------
        query : str
            The guid of the query to run
        """
        url = f"{self.hostname}/manage/query/query?id={query}&output=browser"
        response = self.session.post(url)
        response.raise_for_status()
        return response

    def run_query(self, query: str) -> requests.Response:
        """Enqueue a run of the specified query. This uses Slate's native query queue and scheduling mechanism.


        Parameters
        ----------
        query : str (guid)
            The guid of the query to run.

        Returns
        -------
        requests.response
        """
        url = f"{self.hostname}/manage/query/query?id={query}"
        response = self.session.post(url, data={"cmd": "run"})
        response.raise_for_status()
        return response

    def force_run_query(self, query: str) -> requests.Response:
        """Force a query to run instantly. Results will be delivered to the sftp destination configured for the query.
        The filename that is generated will be returned in the response text.

        Parameters
        ----------
        query : str (guid)
            The guid of the query to run.


        Returns
        -------
        requests.response
        """
        url = f"{self.hostname}/manage/service/export?id={query}"
        response = self.session.get(url)
        response.raise_for_status()
        return response


class Query:
    """
    Class for manipulating a Slate query definition.
    """

    def __init__(
        self, guid: str, session: SlateSession, backend_webservice: str = None
    ):
        self.guid = guid
        self.session = session
        self.backend_webservice = backend_webservice

    @property
    def current_config(self):
        r = self.session.get(self.backend_webservice.format(guid=self.guid))
        r.raise_for_status()
        return r.json()["row"][0]

    @property
    def notes(self):
        return self.current_config.get("notes")

    @property
    def config(self):
        return self.current_config.get("config")

    @config.setter
    def config(self, pkv_dict: dict):
        hostname = self.session.headers.get("Origin")
        route = f"{hostname}/manage/query/build?id={self.guid}&cmd=export"
        payload = {"cmd": "save"}
        for k, v in pkv_dict.items():
            payload[k.replace("export_", "")] = v
        r = self.session.post(route, data=payload)
        r.raise_for_status()

    @property
    def xml(self):
        return self.current_config.get("xml")

    @property
    def name(self):
        return self.current_config.get("name")

    @notes.setter
    def notes(self, notes: str):
        hostname = self.session.headers.get("Origin")
        route = f"{hostname}/manage/query/query?id={self.guid}&cmd=notes"
        payload = {"cmd": "save", "notes": notes}
        r = self.session.post(route, data=payload)
        r.raise_for_status()
