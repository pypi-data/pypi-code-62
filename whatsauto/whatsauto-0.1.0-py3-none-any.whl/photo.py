#!/usr/bin/env python
"""Class for representing a photo in chat"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from whatsauto import WhatsAutoObject


@dataclass
class Photo(WhatsAutoObject):
    caption: Optional[str] = None
    time: Optional[datetime] = None
