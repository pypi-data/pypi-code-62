from flask import Flask, request
from .users import users
from ._defaults import Defaults

def auth(domain, **kwArgs):
  auth_app = Flask('cognito_overlay')
  auth_app.config.from_object(Defaults)
  auth_app.config['CUSTOM_DOMAIN'] = domain
  for key in kwArgs:
    auth_app.config['CUSTOM_{}'.format(key.upper())] = kwArgs[key]

  auth_app.register_blueprint(users)

  return auth_app