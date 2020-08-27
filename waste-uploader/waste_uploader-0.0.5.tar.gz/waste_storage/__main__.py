import requests
import json
import ast
import logging
import os
from aws_requests_auth.aws_auth import AWSRequestsAuth
from time import time

# [init logging]
log = logging.getLogger("logger")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

env_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'PROJECT', 'STAGE', 'PLATFORM', 'VERSION', 'BUILD_NUM',
            'RELEASE_NOTES', 'FILE_PATH', 'BUNDLE_ID']

# [START vars declaration]

api_gateway_host = 'vcgdkujh6d.execute-api.eu-central-1.amazonaws.com'
api_gateway_url = "https://" + api_gateway_host


def check_variables():
    check_result = 'success'
    for i in env_vars:
        if i not in os.environ:
            print("Please pass " + i + " as environment variable")
            check_result = 'failed'
    return check_result


def aws_auth():
    aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    auth = AWSRequestsAuth(aws_access_key=aws_access_key,
                           aws_secret_access_key=aws_secret_access_key,
                           aws_host=api_gateway_host,
                           aws_region='eu-central-1',
                           aws_service='execute-api')
    print("auth successful")
    return auth


def request_upload(auth):
    project = os.environ['PROJECT']
    platform = os.environ['PLATFORM']
    request_upload_url = api_gateway_url + "/prod/" + "upload?project=" + project + "&platform=" + platform
    try:
        r = requests.post(request_upload_url, verify=True, auth=auth)
        response_dict = json.loads(r.text)
        upload_url = response_dict['upload_url']
        clean_hash = response_dict['hash']
        hash = ast.literal_eval(clean_hash)
        print("upload url successfully requested")
        return {'upload_url': upload_url, 'hash': hash}
    except Exception as e:
        log.exception("There is exception during requesting upload url: {}".format(e))
        print("problem with requesting upload url")


def upload(upload_url):
    file_path = os.environ['FILE_PATH']
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            http_response = requests.put(upload_url, files=files)
        # If successful, returns HTTP status code 200
        logging.info(f'File upload HTTP status code: {http_response.status_code}')
        print("binary uploaded")
        return http_response.status_code
    except Exception as e:
        log.exception("There is exception during uploading binary: {}".format(e))
        print("problem with binary uploading")


def distribute(auth, hash):
    project = os.environ['PROJECT']
    stage = os.environ['STAGE']
    platform = os.environ['PLATFORM']
    version = os.environ['VERSION']
    build_num = os.environ['BUILD_NUM']
    release_notes = os.environ['RELEASE_NOTES']
    bundle_id = os.environ['BUNDLE_ID']
    distribute_url = api_gateway_url + "/prod/" + "distribute?project=" + project + "&stage=" + stage + "&platform=" + \
                     platform + "&version=" + version + "&build_num=" + build_num + "&hash=" + hash + "&bundle_id=" + \
                     bundle_id
    try:
        payload = {'release_notes': release_notes}
        d = requests.post(distribute_url, verify=True, json=payload, auth=auth)
        response_dict2 = json.loads(d.text)
        check = response_dict2['message']
        logging.info(f'Commit upload status check: {check}')
        if check != "passed":
            log.error("Distribute status: {}".format(check))
        print("release distributed")
        return check
    except Exception as e:
        log.exception("There is exception during distributing binary: {}".format(e))
        print("problem with release distribution")


# [START run]

def main():
    start = time()
    check_result = check_variables()
    if check_result == 'success':
        auth = aws_auth()
        result_request_upload = request_upload(auth)
        upload_url = result_request_upload['upload_url']
        hash = result_request_upload['hash']
        upload_invocation = upload(upload_url)
        distribute_invocation = distribute(auth, hash)
        logging.info(time() - start)
    else:
        print("set variable(s) above and try again")
        logging.info(time() - start)


if __name__ == "__main__":
    main()
# [END run]
