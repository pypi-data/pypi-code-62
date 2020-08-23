#!/usr/bin/env python
"""Class for representing a user"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from whatsauto import WhatsAutoObject


@dataclass
class User(WhatsAutoObject):
    name: str
    number: str
    about: Optional[str] = None
    about_last_changed: Optional[date] = None
    last_seen: Optional[datetime] = None
