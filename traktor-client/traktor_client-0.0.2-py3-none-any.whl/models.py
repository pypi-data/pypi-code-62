import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

# Auth


class Auth(BaseModel):
    username: str
    password: str


# Colored


COLOR_RE = re.compile("^#([A-Fa-f0-9]{6})$")


def color_validator(value):
    if COLOR_RE.match(value) is None:
        raise ValueError(f"Invalid color string: {value}")
    return value


class ColoredModel(BaseModel):
    color: str

    @validator("color")
    def validate_color(cls, value):
        return color_validator(value)


class ColoredUpdateModel(BaseModel):
    color: Optional[str] = None

    @validator("color")
    def validate_color(cls, value):
        if value is None:
            return None
        return color_validator(value)


# Project


class Project(ColoredModel):
    id: str
    name: str
    color: str
    created_on: datetime
    updated_on: datetime


class ProjectCreateRequest(ColoredModel):
    name: str


class ProjectUpdateRequest(ColoredUpdateModel):
    name: Optional[str] = None


# Task


class Task(ColoredModel):
    project: str
    id: str
    name: str
    default: bool
    created_on: datetime
    updated_on: datetime


class TaskCreateRequest(ColoredModel):
    name: str
    default: bool


class TaskUpdateRequest(ColoredUpdateModel):
    name: Optional[str] = None
    default: Optional[bool] = None


class Timer(BaseModel):
    project: str
    task: str
    description: str
    notes: str
    running_time: str
    created_on: datetime
    updated_on: datetime
    start_time: datetime
    duration: int
    end_time: Optional[datetime] = None


class Report(BaseModel):
    project: str
    task: str
    duration: int
    running_time: str
