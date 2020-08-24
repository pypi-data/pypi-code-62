import pytest
from atrest.api import API

client = API()

@pytest.fixture(autouse=True)
def setup():
    client = API()

def test_api_create_ticket_fails_with_bad_inputs():

    # Test inputs required
    with pytest.raises(TypeError):
        resp = client.create_ticket()

    # Tests that inputs need to be strings
    with pytest.raises(Exception):
        resp = client.create_ticket('title', 1)
    with pytest.raises(Exception):
        resp = client.create_ticket('', 'description')

