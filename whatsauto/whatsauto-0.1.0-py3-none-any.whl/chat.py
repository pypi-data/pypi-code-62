#!/usr/bin/env python
"""Class for representing chat"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from whatsauto import WhatsAutoObject, User, Group


@dataclass
class Chat(WhatsAutoObject):
    name: str
    number: str
    group: Optional[Group] = None
    user: Optional[User] = None
    is_group: Optional[bool] = False
    last_message: Optional[datetime] = None
    media_count: Optional[int] = 0
    mute_notification: Optional[bool] = False
