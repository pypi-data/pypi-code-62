import base64
import os
from typing import List, Dict, Optional, Sequence

from derobertis_cv.plbuild.paths import IMAGES_PATH
from derobertis_cv.pltemplates.software.project import SoftwareProject
from derobertis_cv.pldata.software.yaml_.config import DISPLAY_TITLES, RENAME_MAP, ADD_DESCRIPTIONS, \
    REPLACE_DESCRIPTIONS, \
    REPLACE_URLS, REPLACE_LOGO_URLS, REPLACE_LOGO_FILES


def apply_modifications_to_projects(projects: List[SoftwareProject],
                                    order: Optional[Sequence[str]] = None) -> List[SoftwareProject]:
    projects_dict = _projects_dict(projects)
    for title, display_title in DISPLAY_TITLES.items():
        if title in projects_dict:
            projects_dict[title].display_title = display_title
    for title, add_to_description in ADD_DESCRIPTIONS.items():
        if title in projects_dict:
            projects_dict[title].description += add_to_description
    for title, replace_description in REPLACE_DESCRIPTIONS.items():
        if title in projects_dict:
            projects_dict[title].description = replace_description
    for old_title, new_title in RENAME_MAP.items():
        if old_title in projects_dict:
            projects_dict[old_title].title = new_title
    for title, replace_url in REPLACE_URLS.items():
        if title in projects_dict:
            projects_dict[title].url = replace_url
    for title, replace_url in REPLACE_LOGO_URLS.items():
        if title in projects_dict:
            projects_dict[title].logo_url = replace_url
    for title, file_name in REPLACE_LOGO_FILES.items():
        if title in projects_dict:
            projects_dict[title].logo_url = None
            projects_dict[title].logo_base64 = _image_base64(file_name)

    # Strip extra spacing on descriptions
    for project in projects_dict.values():
        if project.description is None:
            project.description = ''
        project.description = project.description.strip()


    projects = list(projects_dict.values())

    if order is not None:
        projects.sort(key=lambda proj: order.index(proj.title) if proj.title in order else 100)  # type: ignore

    for project in projects:
        # Refresh contents in projects
        contents = project._get_contents()
        project.add_data_from_content(contents)
        project.contents = project.format_contents(contents)

    return projects


def _projects_dict(projects: List[SoftwareProject]) -> Dict[str, SoftwareProject]:
    return {project.title: project for project in projects}


def _image_base64(file_name: str) -> str:
    _, file_extension = os.path.splitext(file_name)
    file_extension = file_extension[:1]  # remove . at beginning
    image_type = file_extension.lower()

    file_path = os.path.join(IMAGES_PATH, file_name)
    with open(file_path, 'rb') as f:
        contents = f.read()
    b64 = base64.b64encode(contents).decode('utf8')
    src = f"data:image/{image_type};base64,{b64}"
    return src