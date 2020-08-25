def create_file_chunks(bucket_name, file_pattern, job_uuid, file_headers, integration_settings, delimiter='|'):
    from stratus_api.storage.gcs import download_from_storage, get_filenames_by_pattern
    import os
    import csv
    from datetime import datetime
    chunk_number = 0
    chunk_records = 0
    start = datetime.utcnow().timestamp()
    for file_path in get_filenames_by_pattern(bucket_name=bucket_name, file_path=file_pattern):
        local_path = download_from_storage(bucket_name=bucket_name, file_path=file_path, job_id=job_uuid)
        with open(local_path, 'rt') as f:
            reader = csv.reader(f, delimiter=delimiter)
            for row in reader:
                chunk_file_path = add_row_to_chunk(job_uuid=job_uuid, file_headers=file_headers, row=row,
                                                   delimiter=delimiter, chunk_number=chunk_number)
                delivered_file_path = add_row_to_delivered_path(
                    job_uuid=job_uuid, file_headers=file_headers, row=row,
                    delimiter=delimiter, chunk_number=chunk_number, timestamp=start)
                if chunk_records >= integration_settings['chunk_size']:
                    yield chunk_file_path, delivered_file_path, chunk_number
                    start = datetime.utcnow().timestamp()
                    os.remove(chunk_file_path)
                    os.remove(delivered_file_path)
                    chunk_records = 0
                    chunk_number += 1
        os.remove(local_path)
    if chunk_records > 0:
        yield chunk_file_path, delivered_file_path, chunk_number
        os.remove(chunk_file_path)
        os.remove(delivered_file_path)


def add_row_to_chunk(row, chunk_number, job_uuid, file_headers, delimiter):
    from stratus_api.core.settings import get_settings
    import os
    chunk_path_pattern = os.path.join(get_settings().get('UPLOAD_FOLDER', '/apps/files/'),
                                      '{job_uuid}-{chunk_number}.csv')
    chunk_path = chunk_path_pattern.format(chunk_number=chunk_number, job_uuid=job_uuid)

    return add_to_file(path=chunk_path, row=row, headers=file_headers, delimiter=delimiter)


def add_row_to_delivered_path(row, chunk_number, job_uuid, file_headers, delimiter, timestamp):
    from stratus_api.core.settings import get_settings
    import os
    from stratus_api.integrations.distribution import DELIVERED_SCHEMA
    delivered_path_pattern = os.path.join(get_settings().get('UPLOAD_FOLDER', '/apps/files/'),
                                          'delivered-{job_uuid}-{chunk_number}.csv')
    delivered_path = delivered_path_pattern.format(chunk_number=chunk_number, job_uuid=job_uuid)
    headers = [i['name'] for i in DELIVERED_SCHEMA]
    for segment_uuid, operation in {k: bool(row[k]) for k in file_headers if row['k'] in {'true', 'false'}}.items():
        add_to_file(path=delivered_path, row=dict(
            internal_user_id=row['internal_user_id'],
            external_user_id=row['external_user_id'],
            segment_uuid=segment_uuid,
            id_type=row['id_type'],
            operation=operation,
            policy_uuid=row['policy_uuid'],
            created_ts=timestamp), headers=headers, delimiter=delimiter)
    return delivered_path


def add_to_file(path, row, headers, delimiter):
    import os
    import csv
    if not os.path.isfile(path):
        with open(path, 'wt') as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(headers)
    with open(path, 'a') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(row)
    return path
