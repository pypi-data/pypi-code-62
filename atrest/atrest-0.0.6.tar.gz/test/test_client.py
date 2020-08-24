import pytest
from atrest.client import Client

at = Client()

@pytest.fixture(autouse=True)
def setup():
    at = Client()


def test_exception_on_blank_header_change(setup):
    with pytest.raises(ValueError):
        at.set_headers(username="")
    with pytest.raises(ValueError):
        at.set_headers(api_integration_code="")
    with pytest.raises(ValueError):
        at.set_headers(secret="")


def test_username_header_change(setup):
    assert "apiuser@strivehealth.com" in str(at.get_headers())
    resp = at.set_headers(username="test")
    assert "apiuser@strivehealth.com" not in str(at.get_headers())
