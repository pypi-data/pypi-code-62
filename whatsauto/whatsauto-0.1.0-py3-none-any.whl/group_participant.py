#!/usr/bin/env python
"""Class for representing a group participant"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from whatsauto import WhatsAutoObject


@dataclass
class GroupParticipant(WhatsAutoObject):
    name: str
    is_admin: bool
    number: Optional[str] = None
    about: Optional[str] = None
