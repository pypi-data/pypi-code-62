from weakref import WeakSet
from dataclasses import dataclass, field
from typing import Optional, Sequence, List, Set, Callable

from weakreflist import WeakList

from derobertis_cv.models.category import CategoryModel
from derobertis_cv.models.nested import NestedModel
from derobertis_cv.pltemplates.logo import HasLogo


@dataclass(frozen=True)
class SkillModel(NestedModel, HasLogo):
    title: str
    level: int
    flexible_case: bool = True
    logo_url: Optional[str] = None
    logo_svg_text: Optional[str] = None
    logo_base64: Optional[str] = None
    logo_fa_icon_class_str: Optional[str] = None
    case_lower_func: Callable[[str], str] = lambda x: x.lower()
    case_title_func: Callable[[str], str] = lambda x: x.title()
    case_capitalize_func: Callable[[str], str] = lambda x: x.capitalize()
    parents: Optional[Sequence['NestedModel']] = field(default_factory=lambda: [])
    children: WeakList = field(default_factory=lambda: WeakList())

    def __post_init__(self):
        super().__init__()

    def to_title_case_str(self) -> str:
        if not self.flexible_case:
            return self.title
        return self.case_title_func(self.title)  # type: ignore

    def to_lower_case_str(self) -> str:
        if not self.flexible_case:
            return self.title
        return self.case_lower_func(self.title)  # type: ignore

    def to_capitalized_str(self) -> str:
        if not self.flexible_case:
            return self.title
        return self.case_capitalize_func(self.title)  # type: ignore

    def get_nested_children(self) -> Set['SkillModel']:
        all_children = set()
        child: 'SkillModel'
        for child in self.children:
            all_children.add(child)
            all_children.update(child.get_nested_children())
        return all_children


def first_word_untouched_rest_title(s: str) -> str:
    parts = s.split()
    return f'{parts[0]} {" ".join([part.title() for part in parts[1:]])}'


def first_word_untouched_rest_lower(s: str) -> str:
    parts = s.split()
    return f'{parts[0]} {" ".join([part.lower() for part in parts[1:]])}'


def first_word_untouched_rest_capitalized(s: str) -> str:
    parts = s.split()
    return f'{parts[0]} {" ".join([part.capitalize() for part in parts[1:]])}'