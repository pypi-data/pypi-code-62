
from chime_frb_api.backends import frb_master
import pytest
from requests.exceptions import HTTPError

master = frb_master.FRBMaster(debug=True, base_url="http://localhost:8001")

def test_get_all_candidates():
    candidates = master.candidates.get_all_candidates()
    assert candidates == []
