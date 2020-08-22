# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_drf',
 'pytest_drf.util',
 'tests',
 'tests.pytest_drf',
 'tests.testapp',
 'tests.testapp.views']

package_data = \
{'': ['*']}

modules = \
['pytest', 'LICENSE', 'CHANGELOG']
install_requires = \
['djangorestframework>3',
 'inflection>=0.3.1,<0.4.0',
 'pytest-assert-utils>=0,<1',
 'pytest-common-subject>=1.0,<2.0',
 'pytest-lambda>=1.1,<2.0',
 'pytest>=3.6']

entry_points = \
{'pytest11': ['drf = pytest_drf.plugin']}

setup_kwargs = {
    'name': 'pytest-drf',
    'version': '1.0.4',
    'description': 'A Django REST framework plugin for pytest.',
    'long_description': '# pytest-drf\n\n[![PyPI version](https://badge.fury.io/py/pytest-drf.svg)](https://badge.fury.io/py/pytest-drf)\n[![Build Status](https://travis-ci.org/theY4Kman/pytest-drf.svg?branch=master)](https://travis-ci.org/theY4Kman/pytest-drf)\n\npytest-drf is a [pytest](http://pytest.org) plugin for testing your [Django REST Framework](https://www.django-rest-framework.org/) APIs.\n\npytest-drf aims to do away with clunky setup code and boilerplate for DRF testing, replacing it with declarative scaffolds that encourage small, easy-to-follow tests with single responsibilities.\n\nThis is accomplished by performing one request per test, and providing the response as a fixture. All configuration of the request — the URL, the query params, the HTTP method, the POST data, etc — is also done through fixtures. This leaves the test methods containing only assertions about the response or the state of the app after the request succeeds.\n\nFor example, let\'s consider a public API endpoint that responds with the JSON string "Hello, World!" and a 200 status code to a GET request. Such an endpoint might be written like so\n\n```python\n# example/views.py\n\nfrom rest_framework import permissions\nfrom rest_framework.decorators import api_view, permission_classes\nfrom rest_framework.response import Response\n\n@api_view()\n@permission_classes([permissions.AllowAny])\ndef hello_world(request):\n    return Response(\'Hello, World!\')\n```\n\nLet\'s route it to `/hello`, and give it a name, so we can easily generate URLs for it.\n\n```python\n# example/urls.py\n\nfrom django.urls import path\n\nfrom example import views\n\nurlpatterns = [\n    path(\'hello\', views.hello_world, name=\'hello-world\'),\n]\n```\n\nWith pytest-drf, we\'d verify the behavior of our endpoint with something like this\n\n```python\n# tests/test_hello.py\n\nclass TestHelloWorld(\n    APIViewTest,\n    UsesGetMethod,\n    Returns200,\n):\n    @pytest.fixture\n    def url(self):\n        return reverse(\'hello-world\')\n\n    def test_returns_hello_world(self, json):\n        expected = \'Hello, World!\'\n        actual = json\n        assert expected == actual\n```\n\nWhen we run pytest, we see two tests run\n\n```\n$ py.test\n\ntests/test_hello.py::TestHelloWorld::test_it_returns_200 <- pytest_drf/status.py PASSED [ 50%]\ntests/test_hello.py::TestHelloWorld::test_returns_hello_world PASSED                    [100%]\n```\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theY4Kman/pytest-drf',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
