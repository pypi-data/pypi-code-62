#!/usr/bin/env python
"""Class for representing a message"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from whatsauto import WhatsAutoObject, User


@dataclass
class Message(WhatsAutoObject):
    user: User
    text: Optional[str] = None
    reply_to: Optional[Message] = None
    read: Optional[datetime] = None
    delivered: Optional[datetime] = None
    pending: Optional[bool] = None
    forwarded: Optional[bool] = False
