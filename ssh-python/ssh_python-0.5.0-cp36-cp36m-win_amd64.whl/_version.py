
import json

version_json = '''
{"date": "2020-08-22T11:47:04.597898", "dirty": false, "error": null, "full-revisionid": "465f87613489751cea2612cab4933432365f71f3", "version": "0.5.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

