from nubium_schemas.nubium_shared_apps.eloqua.schema_components import eloqua_cdo_record, eloqua_contact_record, eloqua_cdo_record_unique_field

eloqua_cdo_record_data = {
    "name": "EloquaCdoRecordData",
    "type": "record",
    "fields": [
        {"name": "eloqua_cdo_record", "type": eloqua_cdo_record}
    ]
}

eloqua_cdo_record_update_data = {
    "name": "EloquaCdoRecordUpdateData",
    "type": "record",
    "fields": [
        {"name": "eloqua_cdo_record", "type": eloqua_cdo_record},
        {"name": "eloqua_cdo_record_unique_field", "type": eloqua_cdo_record_unique_field}
    ]
}

eloqua_contact_record_data = {
    "name": "EloquaContactRecordData",
    "type": "record",
    "fields": [
        {"name": "eloqua_contact_record", "type": eloqua_contact_record}
    ]
}

eloqua_retriever_timestamp = {
    "name": "EloquaRetrieverTimestamp",
    "type": "record",
    "fields": [
        {"name": "timestamp", "type": "string", "default": ""}
    ]
}