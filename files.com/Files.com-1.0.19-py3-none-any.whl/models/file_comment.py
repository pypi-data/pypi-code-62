import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FileComment:
    default_attributes = {
        'id': None,     # int64 - File Comment ID
        'body': None,     # string - Comment body.
        'reactions': None,     # array - Reactions to this comment.
        'path': None,     # string - File path.
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FileComment.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FileComment.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   body (required) - string - Comment body.
    def update(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "body" not in params:
            raise MissingParameterError("Parameter missing: body")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "body" in params and not isinstance(params["body"], str):
            raise InvalidParameterError("Bad parameter: body must be an str")
        response, _options = Api.send_request("PATCH", "/file_comments/{id}".format(id=params['id']), params, self.options)
        return response.data

    def delete(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request("DELETE", "/file_comments/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   page - int64 - Current page number.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   path (required) - string - Path to operate on.
def list_for(path, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["path"] = path
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(FileComment,"GET", "/file_comments/files/{path}".format(path=params['path']), params, options)

# Parameters:
#   body (required) - string - Comment body.
#   path (required) - string - File path.
def create(params = {}, options = {}):
    if "body" in params and not isinstance(params["body"], str):
        raise InvalidParameterError("Bad parameter: body must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "body" not in params:
        raise MissingParameterError("Parameter missing: body")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request("POST", "/file_comments", params, options)
    return FileComment(response.data, options)

# Parameters:
#   body (required) - string - Comment body.
def update(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "body" in params and not isinstance(params["body"], str):
        raise InvalidParameterError("Bad parameter: body must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "body" not in params:
        raise MissingParameterError("Parameter missing: body")
    response, options = Api.send_request("PATCH", "/file_comments/{id}".format(id=params['id']), params, options)
    return FileComment(response.data, options)

def delete(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/file_comments/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = {}, options = {}):
    delete(id, params, options)

def new(*args, **kwargs):
    return FileComment(*args, **kwargs)