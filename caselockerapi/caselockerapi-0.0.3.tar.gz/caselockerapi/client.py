import datetime
import shutil
import os
import sys
import getpass
import argparse
import logging

from requests import Session, Request, HTTPError

from caselockerapi.utils import format_url
from caselockerapi.auth import CaseLockerToken

class Client(object):
    def __init__(self, token=False):
        self.session = Session()
        if token:
            self.token = token

    def _auth_headers(self):
        if self.token.expires + datetime.timedelta(minutes=1) < datetime.datetime.now():
            self.token.refresh()
        return {
            'Authorization': 'Bearer {}'.format(self.token),
        }

    def authenticate(self, DOMAIN=None, USERNAME=None, PASSWORD=None):
        login_token = CaseLockerToken(subdomain=DOMAIN, username=USERNAME, password=PASSWORD)
        self.token = login_token

    def request(self, method, url, stream=False, **kwargs):
        prepped_url = url.format(self.token.subdomain)
        headers = self._auth_headers()
        request = Request(method, prepped_url,
                          headers=headers,
                          **kwargs)
        prepped = request.prepare()
        response = self.session.send(prepped, stream=stream)
        try:
            response.raise_for_status()
        except HTTPError as err:
            logging.error(err.response.content)
            #sys.exit(2)
        return response

    def search(self, url, search=None, ordering=None, page=None, per_page=None, **kwargs):
        kwargs_copy = kwargs.copy()
        params = kwargs_copy.pop('params', {})
        params.update({
            'search': search,
            'ordering': ordering,
            'page': page,
            'count': per_page,
        })
        data = self.request('GET', url, params=params, **kwargs_copy).json()
        return SearchResults(self, url, data,
                             search=search,
                             ordering=ordering,
                             per_page=per_page,
                             **kwargs)

class SearchResults(object):
    def __init__(self, client, url, data, search=None, ordering=None, per_page=None, **kwargs):
        self.client = client
        self.url = url
        self.search = search
        self.ordering = ordering
        self.per_page = per_page
        self.kwargs = kwargs
        self._load_data(data)

    def all_results(self):
        results = self
        while True:
            try:
                for result in results.results:
                    yield result
                results = results.get_next_page()
            except:
                print("End of Results")
                break

    def _load_data(self, data):
        self.page = data['page_number']
        self.count = data['count']
        self.num_pages = data['num_pages']
        self.results = data['results']

    def get_page(self, page):
        return self.client.search(self.url,
                                   search=self.search,
                                   ordering=self.ordering,
                                   page=page,
                                   per_page=self.per_page,
                                   **self.kwargs)

    def get_next_page(self):
        return self.get_page(self.page + 1)

    def get_previous_page(self):
        return self.get_page(self.page - 1)

class CaseObject(object):
    BASE_URL = None
    def __init__(self, client):
        self.client = client

    def list(self, search=None, ordering=None, page=1, per_page=25, **kwargs):
        return self.client.search(format_url(self.BASE_URL), search, ordering, page, per_page, **kwargs)

    def get(self, pk, **kwargs):
        return self.client.request('GET', format_url(self.BASE_URL) + "{}/".format(pk), **kwargs).json()

    def post(self, obj, **kwargs):
        return self.client.request('POST', format_url(self.BASE_URL), json=obj, **kwargs).json()

    def patch(self, pk, obj, **kwargs):
        return self.client.request('PATCH', format_url(self.BASE_URL) + "{}/".format(pk), json=obj, **kwargs).json()

    def delete(self, pk, **kwargs):
        return self.client.request('DELETE', format_url(self.BASE_URL) + "{}/".format(pk), **kwargs).json()

    def put(self, pk, obj, **kwargs):
        return self.client.request('PUT', format_url(self.BASE_URL) + "{}/".format(pk), json=obj, **kwargs).json()

class Contact(CaseObject):
    BASE_URL = 'userforms/contacts/'

    def file_upload(self, pk, file, **kwargs):
        return self.client.request('POST', format_url(self.BASE_URL) + '{}/uploadfile/'.format(pk), files=file, **kwargs).json()

    def add_user_form(self, pk, template, party_name='', form_number='', tags=[], **kwargs):
        obj = {
            "formtemplate_id": template,
            "party_name": party_name,
            "form_number": form_number,
            "tags": tags
        }
        return self.client.request('POST', format_url(self.BASE_URL) + '{}/userforms/'.format(pk), json=obj, **kwargs).json()

    def send_invite(self, pk, message_text, **kwargs):
        return self.client.request('POST', format_url(self.BASE_URL) + '{}/sendinvite/'.format(pk), json={"message_text": message_text}, **kwargs).json()

    #downloadFile

class UserForm(CaseObject):
    BASE_URL = 'userforms/userforms/'

    def resend_esign(self, pk, **kwargs):
        return self.client.request('POST', format_url(self.BASE_URL) + '{}/resendesign/'.format(pk), **kwargs).json()

    def save_answer(self, pk, answer, **kwargs):
        return self.client.request('PUT', format_url(self.BASE_URL) + '{}/answer/'.format(pk), json=answer, **kwargs).json()

    def save_file_answer(self, pk, file, **kwargs):
        return self.client.request('PUT', format_url(self.BASE_URL) + '{}/answer/'.format(pk), files=file, **kwargs).json()

    def downloadFileAnswer(self, pk, fieldtype, question, path, list_id=None, **kwargs):
        with self.client.request('GET',
                          format_url('userforms/userforms/{}/download/'.format(
                              pk
                          )),
                          params={
                              'fieldtype_id': question,
                              'question_id': fieldtype,
                              'list_id': list_id
                          },
                          stream=True) as response:
            with open(path, 'wb') as fp:
                shutil.copyfileobj(response.raw, fp)

    #deleteRow

    #changeAnswerStatus

    #getNotes

    def get_esigns(self, pk, **kwargs):
        return self.client.request('GET', format_url(self.BASE_URL) + '{}/esign/'.format(pk), **kwargs).json()

    def get_activity(self, pk, **kwargs):
        return self.client.request('GET', format_url(self.BASE_URL) + '{}/activity/'.format(pk), **kwargs).json()

    def get_answers(self, pk, **kwargs):
        return self.client.request('GET', format_url(self.BASE_URL) + '{}/answers/'.format(pk), **kwargs).json()

    #downloadEsign

    #addNote

    #downloadPdf

    #downloadCsv

class BulkMail(CaseObject):
    BASE_URL = 'notifications/to-client/'

    def send(self, pk, **kwargs):
        return self.client.request('POST', format_url(self.BASE_URL) + '{}/send/'.format(pk), **kwargs).json()

class EmailProblems(CaseObject):
    BASE_URL = 'notifications/problems/'

    #downloadCsv

class FormTemplate(CaseObject):
    BASE_URL = 'forms/templates/'

class Section(CaseObject):
    BASE_URL = 'forms/sections/'

class Question(CaseObject):
    BASE_URL = 'forms/questions/'

class Paragraph(CaseObject):
    BASE_URL = 'forms/paragraphs/'

class Esignature(CaseObject):
    BASE_URL = 'forms/esignature/'

class OptionList(CaseObject):
    BASE_URL = 'forms/optionlists/'

    # addOptions

class FieldType(CaseObject):
    BASE_URL = 'forms/fieldtypes/'

    #named

class Reports(CaseObject):
    BASE_URL = 'reports/reports/'

    #downloadReport

class Users(CaseObject):
    BASE_URL = 'users/users/'

    #resetPassword

class ClientHelper(Client):
    def __init__(self, token=None, parser=None, args=None):
        self.session = Session()
        if token:
            self.token = token
        else:
            if parser is None:
                parser = argparse.ArgumentParser(description='CaseLocker Python Library')
            subgroup = parser.add_argument_group("Authentication", "Authenticating with your CaseLocker Installation")
            subgroup.add_argument("--s", type=str, help="Your CaseLocker Subdomain Name (https://[DOMAIN].litigationlocker.com/)")
            subgroup.add_argument("--u", type=str, help="Your CaseLocker Username")
            subgroup.add_argument("--p", action="store_true", default=False, help="Prompt for Password")
            subgroup.add_argument("--password", type=str, help="Your CaseLocker Password; NOT RECOMMENDED (Commandline Passthrough is Insecure)")
            subgroup.add_argument("--debug", action="store_true", default=False, help="Debug Mode (Localhost Instance Testing)")
            subgroup.add_argument("--log", default=20, help="Specify log level (10 - Debug; 20 - Info [Default]; 30 - Warning; 40 - Error; 50 - Critical)")
            subgroup.add_argument("--port", type=int, default=8000, help="Localhost Port (Default: 8000)")
            self.args = parser.parse_args()

    def authenticate(self, DOMAIN=None, USERNAME=None, PASSWORD=None):
        if self.args.debug:
            os.environ['DEBUG'] = "TRUE"
            os.environ['DEBUG_PORT'] = "{}".format(self.args.port)
        else:
            os.environ['DEBUG'] = ""
        logging.getLogger().setLevel(self.args.log)
        if len(sys.argv) > 1:
            if self.args.s or self.args.u or self.args.p:
                if self.args.s:
                    DOMAIN = self.args.s
                else:
                    logging.error("Subdomain name not provided (--s SUBDOMAIN)")
                    sys.exit(1)
                if self.args.u:
                    USERNAME = self.args.u
                else:
                    logging.error("Username not provided (--u USERNAME)")
                    sys.exit(1)
                if self.args.password:
                    logging.warning("Command line password passthrough is insecure. RECOMMENDED passthrough env variable CASELOCKER_PASSWORD")
                    PASSWORD = self.args.password
                else:
                    if os.environ.get('CASELOCKER_PASSWORD'):
                        PASSWORD = os.environ.get('CASELOCKER_PASSWORD')
                    elif self.args.p:
                        PASSWORD = getpass.getpass(prompt="[INPT] CaseLocker Password for {}@{}: ".format(USERNAME, DOMAIN), stream=None)
                        if PASSWORD is None or PASSWORD is "":
                            logging.error("Password cannot be empty")
                            sys.exit(1)
                    else:
                        logging.error("Password/prompt not provided (--p OR --password PASSWORD OR env var CASELOCKER_PASSWORD)")
                        sys.exit(1)
        super(ClientHelper, self).authenticate(DOMAIN, USERNAME, PASSWORD)
