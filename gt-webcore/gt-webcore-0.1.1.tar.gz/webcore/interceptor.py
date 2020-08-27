# coding:utf-8
from flask import request
from flask import current_app as app
from flask import session

def _before_request():
    pass

def _after_request(response):
    # app.logger.info(response)
    return response

def init_interceptor(app):
    app.before_request(_before_request)
    app.after_request(_after_request)
