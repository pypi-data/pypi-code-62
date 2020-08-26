# example/views.py

from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination

from tests.testapp.models import KeyValue


class KeyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyValue
        fields = (
            'id',
            'key',
            'value',
        )

class KeyValueViewSet(viewsets.ModelViewSet):
    queryset = KeyValue.objects.order_by('id')
    serializer_class = KeyValueSerializer
    pagination_class = PageNumberPagination



# example/urls.py

from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('kv', KeyValueViewSet, basename='key-values')

urlpatterns = [
    path('', include(router.urls)),
]



import pytest

@pytest.fixture(autouse=True)
def _set_urls(settings):
    settings.ROOT_URLCONF = _set_urls.__module__


from typing import Any, Dict

from pytest_common_subject import precondition_fixture
from pytest_drf import (
    ViewSetTest,
    Returns200,
    Returns201,
    Returns204,
    UsesGetMethod,
    UsesDeleteMethod,
    UsesDetailEndpoint,
    UsesListEndpoint,
    UsesPatchMethod,
    UsesPostMethod,
)
from pytest_drf.util import pluralized, url_for
from pytest_lambda import lambda_fixture, static_fixture
from pytest_assert_utils import assert_model_attrs


def express_key_value(kv: KeyValue) -> Dict[str, Any]:
    return {
        'id': kv.id,
        'key': kv.key,
        'value': kv.value,
    }

express_key_values = pluralized(express_key_value)


class DescribeKeyValueViewSet(ViewSetTest):
    list_url = lambda_fixture(
        lambda:
            url_for('key-values-list'))

    detail_url = lambda_fixture(
        lambda key_value:
            url_for('key-values-detail', key_value.pk))

    class DescribeList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        key_values = lambda_fixture(
            lambda: [
                KeyValue.objects.create(key=key, value=value)
                for key, value in {
                    'quay': 'worth',
                    'chi': 'revenue',
                    'umma': 'gumma',
                }.items()
            ],
            autouse=True,
        )

        def it_returns_key_values(self, key_values, results):
            expected = express_key_values(sorted(key_values, key=lambda kv: kv.id))
            actual = results
            assert expected == actual

    class DescribeCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        data = static_fixture({
            'key': 'snakes',
            'value': 'hissssssss',
        })

        initial_key_value_ids = precondition_fixture(
            lambda:
                set(KeyValue.objects.values_list('id', flat=True)))

        def it_creates_new_key_value(self, initial_key_value_ids, json):
            expected = initial_key_value_ids | {json['id']}
            actual = set(KeyValue.objects.values_list('id', flat=True))
            assert expected == actual

        def it_sets_expected_attrs(self, data, json):
            key_value = KeyValue.objects.get(pk=json['id'])

            expected = data
            assert_model_attrs(key_value, expected)

        def it_returns_key_value(self, json):
            key_value = KeyValue.objects.get(pk=json['id'])

            expected = express_key_value(key_value)
            actual = json
            assert expected == actual


    class DescribeRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        key_value = lambda_fixture(
            lambda:
                KeyValue.objects.create(
                    key='monty',
                    value='jython',
                ))

        def it_returns_key_value(self, key_value, json):
            expected = express_key_value(key_value)
            actual = json
            assert expected == actual

    class DescribeUpdate(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        key_value = lambda_fixture(
            lambda:
                KeyValue.objects.create(
                    key='pipenv',
                    value='was a huge leap forward',
                ))

        data = static_fixture({
            'key': 'buuut poetry',
            'value': 'locks quicker and i like that',
        })

        def it_sets_expected_attrs(self, data, key_value):
            # We must tell Django to grab fresh data from the database, or we'll
            # see our stale initial data and think our endpoint is broken!
            key_value.refresh_from_db()

            expected = data
            assert_model_attrs(key_value, expected)

        def it_returns_key_value(self, key_value, json):
            key_value.refresh_from_db()

            expected = express_key_value(key_value)
            actual = json
            assert expected == actual

    class DescribeDestroy(
        UsesDeleteMethod,
        UsesDetailEndpoint,
        Returns204,
    ):
        key_value = lambda_fixture(
            lambda:
                KeyValue.objects.create(
                    key='i love',
                    value='YOU',
                ))

        initial_key_value_ids = precondition_fixture(
            lambda key_value:  # ensure our to-be-deleted KeyValue exists in our set
                set(KeyValue.objects.values_list('id', flat=True)))

        def it_deletes_key_value(self, initial_key_value_ids, key_value):
            expected = initial_key_value_ids - {key_value.id}
            actual = set(KeyValue.objects.values_list('id', flat=True))
            assert expected == actual
