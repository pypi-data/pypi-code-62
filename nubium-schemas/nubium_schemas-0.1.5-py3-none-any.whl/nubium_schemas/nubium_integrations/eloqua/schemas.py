from nubium_schemas.nubium_integrations.eloqua.schema_components import (ebb_job_init_fields,
                                                                         ebb_job_eloqua_metadata,
                                                                         ebb_worker_task_fields)

ebb = {
    "name": "EloquaBulkBatcher",
    "type": "record",
    "fields": [
        {"name": "controller_job_id", "type": "string", "default": ""},
        {"name": "controller_job_status_update", "type": "string", "default": ""},
        {"name": "job_init_fields", "type": ebb_job_init_fields},
        {"name": "job_eloqua_metadata", "type": ebb_job_eloqua_metadata},
        {"name": "worker_task_fields", "type": ebb_worker_task_fields}
    ]
}
