# example/views.py

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response



@api_view()
@permission_classes([permissions.AllowAny])
def hello_world(request):
    return Response('Hello, World!')



# example/urls.py

from django.urls import path

urlpatterns = [
    path('hello', hello_world, name='hello-world'),
]


import pytest
from django.urls import reverse
from pytest_drf import APIViewTest, Returns200, UsesGetMethod


class TestHelloWorld(
    APIViewTest,
    UsesGetMethod,
    Returns200,
):
    @pytest.fixture(autouse=True)
    def _set_urls(self, settings):
        settings.ROOT_URLCONF = self.__class__.__module__

    @pytest.fixture
    def url(self):
        return reverse('hello-world')

    def test_returns_hello_world(self, json):
        expected = 'Hello, World!'
        actual = json
        assert expected == actual
