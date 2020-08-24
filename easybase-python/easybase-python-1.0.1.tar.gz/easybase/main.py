import requests

def _generateBareUrl(integrationType, integrationID):
    return r'https://api.easybase.io/' + integrationType + r"/" + integrationID

def get(integrationID: str, offset: int=None, limit: int=None, authentication: int=None, customQuery: dict={}):
    body = {}
    body.update(customQuery)
    if offset != None: body['offset'] = offset
    if limit != None: body['limit'] = limit
    if authentication != None: body['authentication'] = authentication

    try:
        r = requests.post(_generateBareUrl('get', integrationID), json=body)
        return r.json()
    except Exception as e:
        print("EasyBase exception: {}".format(e))
        return e


def post(integrationID: str, newRecord: dict, authentication: str=None, insertAtEnd: bool=None):
    body = {}
    body.update(newRecord)
    if authentication != None: body['authentication'] = authentication
    if insertAtEnd != None: body['insertAtEnd'] = insertAtEnd

    try:
        r = requests.post(_generateBareUrl('post', integrationID), json=body)
        return r.json()['message']
    except Exception as e:
        print("EasyBase exception: {}".format(e))
        return e


def update(integrationID: str, updateValues: dict, authentication: int=None, customQuery: dict={}):
    body = { "updateValues": updateValues }
    body.update(customQuery)
    if authentication != None: body['authentication'] = authentication

    try:
        r = requests.post(_generateBareUrl('update', integrationID), json=body)
        return r.json()['message']
    except Exception as e:
        print("EasyBase exception: {}".format(e))
        return e


def delete(integrationID: str, authentication: int=None, customQuery: dict={}):
    body = {}
    body.update(customQuery)
    if authentication != None: body['authentication'] = authentication

    try:
        r = requests.post(_generateBareUrl('delete', integrationID), json=body)
        return r.json()['message']
    except Exception as e:
        print("EasyBase exception: {}".format(e))
        return e