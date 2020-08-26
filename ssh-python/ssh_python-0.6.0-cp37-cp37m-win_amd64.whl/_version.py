
import json

version_json = '''
{"date": "2020-08-26T16:56:30.247200", "dirty": false, "error": null, "full-revisionid": "e2d4bca1bd24781a87d7d7089e9f912eca2679fb", "version": "0.6.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

