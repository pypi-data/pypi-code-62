import json
import os

from krautmarkt.core.models import SaveModel
from loguru import logger
from slugify import slugify


class SaveHugo(SaveModel):
    """
    SaveHugo saves the dataset files from source as Hugo files
    """

    def __init__(
        self,
        metas,
        json_path=None,
        markdown_path=None,
        project_path=None,
        markdown_data_endpoint=None,
    ) -> None:

        if markdown_data_endpoint is None:
            markdown_data_endpoint = "metadata.json"
        if project_path is None:
            project_path = "."

        if json_path is None:
            json_path = os.path.join("data", "markt")
        if markdown_path is None:
            markdown_path = os.path.join("content", "markt")

        super().__init__(metas, json_path, markdown_path, project_path)
        self.markdown_data_endpoint = markdown_data_endpoint

    @staticmethod
    def _save_one_json(dic, path) -> None:
        """
        _save_one_json saves the dictionary of metadata as json file
        """

        logger.info(f"Will save {dic} to {path}")
        with open(path, "w+") as fp:
            json.dump(dic, fp)

        logger.info(f"Saved {dic} to {path}")

    @staticmethod
    def _generate_markdown_list_meta(dic_lists, name) -> str:
        """
        _markdown_metadata_entry
        """

        if dic_lists:
            md_hugo = f"{name}:"
            for l in dic_lists:
                md_hugo = md_hugo + f'\n  - "{l}"'
            md_hugo = md_hugo + "\n"
        else:
            md_hugo = ""

        return md_hugo

    def save_one_markdown(self, dic, path, markdown_data_endpoint=None) -> None:
        """
        save_one_markdown generates a markdown file
        """
        if markdown_data_endpoint is None:
            markdown_data_endpoint = self.markdown_data_endpoint

        logger.info(f"Will save {dic} to {path}")

        # generate tilte, description, keywords, and categories
        metadata_title = dic.get("profile")
        metadata_description = dic.get("description")
        metadata_keywords = dic.get("keywords")
        metadata_categories = dic.get("categories", ["MISC"])

        keywords_hugo = self._generate_markdown_list_meta(metadata_keywords, "keywords")
        categories_hugo = self._generate_markdown_list_meta(
            metadata_categories, "categories"
        )

        metadata_hugo = '---\ntitle: "{}"\nendpoint: {}\n'.format(
            metadata_title, markdown_data_endpoint
        )
        if metadata_description:
            metadata_hugo = metadata_hugo + f'description: "{metadata_description}"\n'
        if keywords_hugo:
            metadata_hugo = metadata_hugo + keywords_hugo
        if categories_hugo:
            metadata_hugo = metadata_hugo + categories_hugo

        # end the metadata region
        metadata_hugo = metadata_hugo + "---"

        with open(path, "w") as fp:
            fp.write(metadata_hugo)

        logger.info(f"Saved {dic} to {path}")

    def save_all(self) -> None:
        """
        save_all saves all files necessary
        """

        # attach working directory to all paths
        json_path = os.path.join(self.project_path, self.json_path)
        md_path = os.path.join(self.project_path, self.markdown_path)

        # create folders if necessary
        try:
            os.makedirs(md_path)
            logger.info(f"Created {md_path}")
        except FileExistsError as err:
            logger.info(f"{md_path} already exists!")

        for m in self.metas:
            m_profile = slugify(m.get("profile"))
            m_json_folder = os.path.join(json_path, f"{m_profile}")

            # create folder for the corresponding json file of the dataset
            try:
                os.makedirs(m_json_folder)
                logger.info(f"Created {md_path}")
            except FileExistsError as err:
                logger.info(f"{md_path} already exists!")

            m_json_path = os.path.join(m_json_folder, "metadata.json")
            self._save_one_json(m, m_json_path)

            m_md_path = os.path.join(md_path, f"{m_profile}.md")
            # generate markdown files
            self.save_one_markdown(m, m_md_path)


if __name__ == "__main__":

    pass
