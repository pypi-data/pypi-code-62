#!/usr/bin/env python
"""Class for representing a group group"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List

from whatsauto import WhatsAutoObject, GroupParticipant


@dataclass
class Group(WhatsAutoObject):
    name: str
    description: Optional[str] = None
    created_by: Optional[str] = None
    created_date: Optional[date] = None
    participants: List[GroupParticipant] = field(default_factory=list)
