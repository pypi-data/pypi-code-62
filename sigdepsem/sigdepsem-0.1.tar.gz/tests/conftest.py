from typing import NamedTuple, Callable

import pytest
from sigdepsem import SigDepMeta, signature_dependent_semantics


class ClassSetup(NamedTuple):
    decorator: Callable[[type], type]
    meta: type


@pytest.fixture(params=[
    ClassSetup(signature_dependent_semantics, type),
    ClassSetup(lambda cls: cls, SigDepMeta),
])
def class_setup(request):
    return request.param


@pytest.fixture
def decorator(class_setup: ClassSetup):
    return class_setup.decorator


@pytest.fixture
def meta(class_setup: ClassSetup):
    return class_setup.meta
