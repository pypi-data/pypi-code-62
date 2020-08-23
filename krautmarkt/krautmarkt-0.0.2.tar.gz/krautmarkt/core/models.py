from abc import abstractclassmethod
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


class SourceModel:
    """
    Model is the base class for
    """

    def __init__(self, path_to_datasets: str) -> None:
        self.path_to_datasets = path_to_datasets
        self.metas = []

    @abstractclassmethod
    def fetch_metadata(self):
        raise NotImplementedError(f"Please implement this method")


class SaveModel:
    """
    SaveModel take the models and save them as files to serve as the database.
    """

    def __init__(self, metas, json_path, markdown_path, project_path) -> None:

        self.json_path = json_path
        self.markdown_path = markdown_path
        self.metas = metas
        self.project_path = project_path

    @abstractclassmethod
    def save_json(self) -> None:
        raise NotImplementedError("Please implement save_json method")

    @abstractclassmethod
    def save_markdown(self) -> None:
        raise NotImplementedError("Please implement save_markdown method")

    @abstractclassmethod
    def save_all(self) -> None:
        raise NotImplementedError("Please implement save_all method")
