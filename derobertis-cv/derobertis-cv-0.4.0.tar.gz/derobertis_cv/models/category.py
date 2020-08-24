from dataclasses import dataclass
from typing import Optional

from derobertis_cv.pltemplates.logo import HasLogo


@dataclass
class CategoryModel(HasLogo):
    title: str
    logo_url: Optional[str] = None
    logo_svg_text: Optional[str] = None
    logo_base64: Optional[str] = None
    logo_fa_icon_class_str: Optional[str] = None
