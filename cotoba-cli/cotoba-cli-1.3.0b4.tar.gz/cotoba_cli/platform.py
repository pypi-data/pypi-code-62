import base64
import boto3
import http.client
import json
import logging
import os
import pytz
import re

import click

from datetime import datetime
from pytz import timezone

from botocore import exceptions as boto_exceptions
from urllib.parse import urljoin

from cotoba_cli import config
from cotoba_cli import cognito
from cotoba_cli.util import api_session


logger = logging.getLogger(__name__)
client = boto3.client('cognito-idp',
                      region_name=cognito.USER_POOL_REGION,
                      aws_access_key_id=cognito.ACCESS_KEY,
                      aws_secret_access_key=cognito.SECRET_KEY,
                      )

BOT_API_PATH = 'bots/'


class PlatformResponse:
    def __init__(self,
                 response_body_json,
                 http_status_code,
                 message_text,
                 request_body=None,
                 response_headers=None):
        self.__response_body_json = response_body_json
        self.__http_status_code = http_status_code
        self.__message_text = message_text
        self.__response_headers = response_headers
        self.__request_body = request_body

    def get_response_body(self):
        return json.loads(self.__response_body_json)

    @property
    def message(self):
        return self.__message_text

    @message.setter
    def message(self, message):
        self.__message_text = message

    def print_message(self, output_headers):
        if not (self.__message_text or output_headers):
            return
        if output_headers:
            try:
                body = json.loads(self.__message_text)
            except json.decoder.JSONDecodeError:
                body = self.__message_text
            response = {
                'headers': dict(self.__response_headers),
                'body': body
            }
            click.echo(json.dumps(response))
        else:
            click.echo(self.__message_text)

    def print(self, print_status=True, output_headers=False):
        if print_status:
            if 400 <= self.__http_status_code:
                color = 'red'
            else:
                color = 'green'
            status_msg = http.client.responses[self.__http_status_code]
            status_text = str(self.__http_status_code) + ' ' + status_msg
            click.echo(click.style(
                status_text,
                fg=color),
                err=True
            )
        self.print_message(output_headers)

    def get_request_time(self):
        return self.__request_body.get('time')

    @staticmethod
    def build_from_requests_result(result, message=None, request_body=None):
        message = message if message is not None else result.text
        return PlatformResponse(result.text,
                                result.status_code,
                                message,
                                request_body=request_body,
                                response_headers=result.headers)


def login(login_id, password):
    authorization = config.load()['default'].get('authorization')
    if not authorization:
        raise click.BadParameter('Authorization Id is required.', param_hint='configuration')
    pool_id, client_id = decode_cognito_setting(authorization)

    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': login_id,
                'PASSWORD': password
            },
            ClientId=client_id
        )
    except client.exceptions.NotAuthorizedException:
        raise click.BadParameter('Password Incorrect', param_hint='password')
    except boto_exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            raise click.BadParameter(f'Account with id({login_id}) is not found.',
                                     param_hint='id')
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise click.BadParameter(e.response['Error']['Message'], param_hint='id/password')

        # TODO: Add error for expired refresh token.
        else:
            raise e

    return response


def change_password(old_password, new_password, access_token):
    try:
        client.change_password(
            PreviousPassword=old_password,
            ProposedPassword=new_password,
            AccessToken=access_token
        )
    except boto_exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidPasswordException':
            error_message_all = str(e.response['Error']['Message'])
            result = re.match('(.*: )(?P<message>.*$)', error_message_all)
            if result is not None:
                raise click.BadParameter(result.group('message'), param_hint='new password')
            else:
                raise click.BadParameter('Invalid Password.', param_hint='new password')
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise click.UsageError(e.response['Error']['Message'])
        elif e.response['Error']['Code'] == 'LimitExceededException':
            raise click.UsageError(e.response['Error']['Message'])
        else:
            raise e
    except boto_exceptions.ParamValidationError as e:
        raise e


def create_bot(auth,
               filepath,
               endpoint_url,
               name=None,
               message=None,
               nlu_url=None,
               nlu_api_key=None):
    if not os.path.exists(filepath) or os.path.isdir(filepath):
        raise click.BadParameter(f'File {filepath} not found.')
    with open(filepath, 'rb') as f:
        encoded_file = base64.b64encode(f.read()).decode('utf-8')
    headers = {
        'Authorization': auth.id_token,
        'Content-Type': 'application/json; charset=utf-8'
    }
    body = {
        'file': encoded_file,
        'name': name,
        'message': message,
        'nluUrl': nlu_url,
        'nluApiKey': nlu_api_key
        }
    body = {k: v for k, v in body.items() if v is not None}
    r = api_session().post(
        urljoin(endpoint_url, BOT_API_PATH),
        json.dumps(body),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def update_bot(auth,
               bot_id,
               endpoint_url,
               filepath=None,
               name=None,
               message=None,
               nlu_url=None,
               nlu_api_key=None):
    headers = {
        'Authorization': auth.id_token,
        'Content-Type': 'application/json; charset=utf-8'
    }

    body = {
        'name': name,
        'message': message,
        'nluUrl': nlu_url,
        'nluApiKey': nlu_api_key
    }

    if filepath:
        try:
            with open(filepath, 'rb') as f:
                body['file'] = base64.b64encode(f.read()).decode('utf-8')
        except OSError as e:
            raise click.UsageError(str(e))

    body = {k: v for k, v in body.items() if v is not None}

    r = api_session().put(
        urljoin(endpoint_url, BOT_API_PATH + bot_id),
        json.dumps(body),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def list_bots(auth, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    r = api_session().get(
        urljoin(endpoint_url, BOT_API_PATH),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def get_bot(auth, bot_id, zipfile_path, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    api_path = urljoin(endpoint_url, BOT_API_PATH + bot_id)
    if zipfile_path:
        api_path = api_path + '?include_scenario=true'

    r = api_session().get(api_path, headers=headers)
    res = PlatformResponse.build_from_requests_result(r)
    if zipfile_path:
        with open(zipfile_path, 'wb') as f:
            f.write(base64.b64decode(res.get_response_body()['file']))
    return res


def delete_bot(auth, bot_id, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    r = api_session().delete(
        urljoin(endpoint_url,  BOT_API_PATH + bot_id),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def generate_ask_url(endpoint_url, bot_id):
    return urljoin(endpoint_url, BOT_API_PATH + bot_id + '/ask')


def ask_bot(
        bot_id,
        api_key,
        user_id,
        utterance,
        topic=None,
        metadata=None,
        log_level=None,
        locale=None,
        endpoint_url=None
):
    """
    Returns:
      (decode_response_text, unicode_response_text, request_time)
    """
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-api-key': api_key
    }
    request_time = get_local_time(locale)
    payload = {
        "locale": locale,
        "time": request_time,
        "userId": user_id,
        "utterance": utterance,
    }
    if log_level is not None:
        payload['config'] = {"logLevel": log_level}
    if topic is not None:
        payload['topic'] = topic
    if metadata is not None:
        payload['metadata'] = metadata

    r = api_session().post(
        generate_ask_url(endpoint_url, bot_id),
        data=json.dumps(payload),
        headers=headers
    )

    return PlatformResponse.build_from_requests_result(
        r,
        request_body=payload)


def debug_bot(auth, bot_id, api_key, endpoint_url, user_id=None):
    headers = {
        'Authorization': auth.id_token,
        'x-api-key': api_key
    }

    if user_id is None:
        user_id = "None"

    r = api_session().post(
        urljoin(endpoint_url,  BOT_API_PATH + bot_id + '/debug'),
        json.dumps({
            'userId': user_id
        }),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def create_api_key(auth,
                   bot_id,
                   expiration_days,
                   max_api_calls,
                   description,
                   endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }

    request_body = {
        'expirationDays': expiration_days,
        'maxApiCalls': max_api_calls,
        'description': description,
    }

    r = api_session().post(
        urljoin(endpoint_url,  BOT_API_PATH + bot_id + '/api-keys'),
        json.dumps(request_body),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def list_api_keys(auth, bot_id, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }

    r = api_session().get(
        urljoin(endpoint_url,  BOT_API_PATH + bot_id + '/api-keys'),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def get_api_key(auth, bot_id, api_key, endpoint_url):
    headers = {
        'Authorization': auth.id_token,
    }

    r = api_session().get(
        urljoin(
            endpoint_url,
            BOT_API_PATH + bot_id + '/api-keys/' + api_key
        ),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def update_api_key(auth,
                   bot_id,
                   api_key,
                   description,
                   endpoint_url):
    headers = {
        'Authorization': auth.id_token,
    }

    request_body = {}

    if description is not None:
        request_body['description'] = description

    r = api_session().put(
        urljoin(
            endpoint_url,
            BOT_API_PATH + bot_id + '/api-keys/' + api_key
        ),
        json.dumps(request_body),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def delete_api_key(auth, bot_id, api_key, endpoint_url):
    headers = {
        'Authorization': auth.id_token,
        'x-api-key': api_key
    }

    r = api_session().delete(
        urljoin(
            endpoint_url,
            BOT_API_PATH + bot_id + '/api-keys/' + api_key
        ),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def run_bot(auth, bot_id, update, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    api_path = urljoin(endpoint_url, BOT_API_PATH + bot_id + '/run')
    if update:
        api_path = api_path + '?update=true'

    r = api_session().post(
        api_path,
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def stop_bot(auth, bot_id, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }

    r = api_session().post(
        urljoin(endpoint_url, BOT_API_PATH + bot_id + '/stop'),
        headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def encode_cognito_setting(pool_id, client):
    connected_text = ','.join([pool_id, client])
    encoded_text = base64.encodebytes(connected_text.encode('ascii'))
    return encoded_text


def decode_cognito_setting(encoded_cognito_setting):
    """
    Returns:
      (pool_id, client_id)
    """
    if type(encoded_cognito_setting) is str:
        encoded_cognito_setting = encoded_cognito_setting.encode('ascii')
    try:
        decoded_text = base64.decodebytes(
            encoded_cognito_setting).decode('ascii')
    except base64.binascii.Error:
        raise click.BadParameter('Invalid id', param_hint='authorization id')
    if decoded_text.count(',') != 1:
        # TODO: add debug message
        raise click.BadParameter('Invalid id', param_hint='authorization id')
    return tuple(decoded_text.strip().split(','))


def get_local_time(locale):
    result = re.match('(?P<lang>.*)[_|-](?P<code>.*)', locale)
    country_code = result.group('code')
    tz_dict = pytz.country_timezones
    tz = tz_dict.get(country_code)
    return datetime.now(timezone(tz[0])).isoformat(timespec='seconds')


def get_bot_logs(auth, endpoint_url,
                 start_date=None,
                 end_date=None,
                 limit=None,
                 offset=None,
                 bot_id=None,
                 api_key_id=None,
                 ):
    headers = {
        'Authorization': auth.id_token
    }
    params = {'start': start_date, 'end': end_date,
              'limit': limit, 'offset': offset,
              'bot_id': bot_id, 'api_key_id': api_key_id}
    r = api_session().get(
        urljoin(endpoint_url, BOT_API_PATH + 'logs/dialogues'),
        params=params, headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def get_bot_traffics(auth, endpoint_url,
                     aggregation,
                     start_date=None,
                     end_date=None,
                     bot_id=None,
                     api_key_id=None,
                     ):
    headers = {
        'Authorization': auth.id_token
    }
    params = {'aggregation': aggregation,
              'start': start_date, 'end': end_date,
              'bot_id': bot_id, 'api_key_id': api_key_id}
    r = api_session().get(
        urljoin(endpoint_url, BOT_API_PATH + 'logs/traffics'),
        params=params, headers=headers)
    return PlatformResponse.build_from_requests_result(r)


def get_bot_topics(auth, endpoint_url,
                   aggregation,
                   start_date=None,
                   end_date=None,
                   bot_id=None,
                   api_key_id=None,
                   ):
    headers = {
        'Authorization': auth.id_token
    }
    params = {'aggregation': aggregation,
              'start': start_date, 'end': end_date,
              'bot_id': bot_id, 'api_key_id': api_key_id}
    r = api_session().get(
        urljoin(endpoint_url, BOT_API_PATH + 'logs/topics'),
        params=params, headers=headers)
    return PlatformResponse.build_from_requests_result(r)
