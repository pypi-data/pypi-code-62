from flask import Flask
from flask import Response
from flask import jsonify
from flask.json import JSONEncoder

from sqlalchemy.orm.collections import InstrumentedList

from sqlalchemy_abc import serialize
from sqlalchemy_abc import iserialize


class ModelEncoder(JSONEncoder):
    def default(self, data):
        if isinstance(data, InstrumentedList):
            collection = serialize(data)
        else:
            data = iserialize(data)
        return data
        return JSONEncoder.default(self, data)


class JSONResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        elif isinstance(rv, tuple):
            rv = jsonify(rv[0]), rv[1]
        return super(JSONResponse, cls).force_type(rv, environ)


class FlaskJSON(Flask):
    response_class = JSONResponse
    json_encoder = ModelEncoder

