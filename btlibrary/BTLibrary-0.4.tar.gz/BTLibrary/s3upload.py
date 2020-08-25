import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json

def s3upload(endpoint:str, api_key:str, payload:str):
    hdr = {'Content-Type':'application/json','x-api-key':api_key}
    sess = requests.Session()
    retries = Retry(total=5, backoff_factor=.1)
    sess.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        resp = sess.post(endpoint, headers=hdr, timeout=30)

        resp.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return http_err
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return err
    else:
        print('Successful response for cloud urls.')
        response = json.loads(resp.json()['body'])
        files = {'file': (response['fields']['key'], payload)}

    try:
        http_response = sess.post(response['url_upload'], data=response['fields'],files=files, timeout=30)
        http_response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return http_err
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return err
    else:
        print('Successful response payload dispatch.')
        return {'response_urls':resp.json(),'response_upload_status_code':http_response.status_code}
