import json


def get_message_body_from_record(record: dict) -> dict:
    try:
        return json.loads(record.get('body'))
    except ValueError:
        return {}
