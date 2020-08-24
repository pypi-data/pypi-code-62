eloqua_cdo_record = {
    "name": "EloquaCdoRecord",
    "type": "record",
    "fields": [
        {"name": "cdo_id", "type": "string", "default": ""},
        {"name": "cdo_record_id", "type": "string", "default": ""},
        {"name": "field_map", "type": {"type": "map", "values": "string"}, "default": "{}"}
    ]
}

eloqua_cdo_record_unique_field = {
    "name": "EloquaCdoRecordUniqueField",
    "type": "record",
    "fields": [
        {"name": "cdo_unique_field", "type": "string", "default": ""},
        {"name": "record_unique_field_value", "type": "string", "default": ""}
    ]
}

eloqua_contact_record = {
    "name": "EloquaContactRecord",
    "type": "record",
    "fields": [
        {"name": "contact_id", "type": "string", "default": ""},
        {"name": "field_map", "type": {"type": "map", "values": "string"}, "default": "{}"}
    ]
}