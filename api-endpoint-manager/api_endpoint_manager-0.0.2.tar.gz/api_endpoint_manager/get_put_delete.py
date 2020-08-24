from flask_jwt_auth import APIAuth
from flask_restplus import Resource
from http_request_args.validation import RequestArgsValidator
from http_request_response import RequestUtilities

from .api_endpoint import APIEndpoint


class GetPutDeleteEndpoints(APIEndpoint):
    def __init__(self, api, route,
                 get_qs_args_def, get_body_args_def, get_business_class,
                 put_qs_args_def, put_body_args_def, put_business_class,
                 delete_qs_args_def, delete_body_args_def, delete_business_class,
                 get_authorization_object=None, put_authorization_object=None, delete_authorization_object=None):

        if '_id' in route:
            @api.route(route)
            class SingleItem(Resource):

                @RequestUtilities.try_except
                @RequestArgsValidator.args_validation(get_qs_args_def, get_body_args_def)
                @APIAuth.auth_required(authorization_object=get_authorization_object)
                def get(self, _id):
                    return get_business_class.run()

                @RequestUtilities.try_except
                @RequestArgsValidator.args_validation(put_qs_args_def, put_body_args_def)
                @APIAuth.auth_required(authorization_object=put_authorization_object)
                def put(self, _id):
                    return put_business_class.run()

                @RequestUtilities.try_except
                @RequestArgsValidator.args_validation(delete_qs_args_def, delete_body_args_def)
                @APIAuth.auth_required(authorization_object=delete_authorization_object)
                def delete(self, _id):
                    return delete_business_class.run()
        else:
            @api.route(route)
            class SingleItem(Resource):
                @RequestUtilities.try_except
                @RequestArgsValidator.args_validation(get_qs_args_def, get_body_args_def)
                @APIAuth.auth_required(authorization_object=get_authorization_object)
                def get(self):
                    return get_business_class.run()

                @RequestUtilities.try_except
                @RequestArgsValidator.args_validation(put_qs_args_def, put_body_args_def)
                @APIAuth.auth_required(authorization_object=put_authorization_object)
                def put(self):
                    return put_business_class.run()

                @RequestUtilities.try_except
                @RequestArgsValidator.args_validation(delete_qs_args_def, delete_body_args_def)
                @APIAuth.auth_required(authorization_object=delete_authorization_object)
                def delete(self):
                    return delete_business_class.run()
