UPLOADED_FILE_GCS_PATH_FORMAT = "{job_uuid}/uploaded.{chunk_number}.csv"
DELIVERED_SCHEMA = [
    dict(name='segment_uuid', type='STRING'),
    dict(name='internal_user_id', type='STRING'),
    dict(name='external_user_id', type='STRING'),
    dict(name='id_type', type='STRING'),
    dict(name='operation', type='BOOLEAN'),
    dict(name='created_ts', type='STRING'),
]


def deliver_data(job_uuid, bucket_name, file_pattern, platform_name, destination, file_headers, segments, id_types,
                 operations,
                 **kwargs):
    from stratus_api.integrations import get_integration_function, get_integration_settings
    from stratus_api.integrations.chunks import create_file_chunks
    from datetime import datetime
    start_time = datetime.utcnow()
    distribute_file = get_integration_function(function_name='distribute_file')
    segment_mapping = {i['segment_uuid']: i for i in segments}
    for local_path, delivered_path, chunk_number, in create_file_chunks(
            bucket_name=bucket_name,
            file_pattern=file_pattern,
            integration_settings=get_integration_settings(),
            file_headers=file_headers,
            job_uuid=job_uuid):
        try:
            success = distribute_file(
                destination=destination, platform_name=platform_name, segments=segment_mapping, local_path=local_path,
                chunk_number=chunk_number, start_time=start_time,
            )
        except Exception as e:
            success = False
        if success:
            load_delivered_data(
                local_path=delivered_path,
                job_uuid=job_uuid,
                chunk_number=chunk_number
            )
    return close_delivery(job_uuid=job_uuid)


def load_delivered_data(job_uuid, local_path, chunk_number):
    from stratus_api.storage.gcs import upload_file_to_gcs
    upload_file_to_gcs(
        local_path=local_path,
        file_path=UPLOADED_FILE_GCS_PATH_FORMAT.format(
            job_uuid=job_uuid,
            chunk_number=chunk_number
        )
    )
    return True


def close_delivery(job_uuid):
    from stratus_api.bigquery import load_csv_to_bq_table
    from stratus_api.core.settings import get_settings
    from stratus_api.core.common import generate_random_id
    load_csv_to_bq_table(
        bucket=get_settings()['bucket_name'],
        external_job_id=generate_random_id(),
        file_patterns=[
            UPLOADED_FILE_GCS_PATH_FORMAT.format(job_uuid=job_uuid, chunk_number='*')
        ],
        table_name=get_settings()['delivered_data_table_name'],
        dataset_name=get_settings()['delivered_data_dataset_name'],
        project_id=get_settings()['delivered_data_project_id'],
        schema=DELIVERED_SCHEMA, headers=False
    )
    return job_uuid, True
