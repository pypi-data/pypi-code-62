# coding: utf-8

"""
    Bedrock

    API documentation for Bedrock platform  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from bdrk.v1.api_client import ApiClient
from bdrk.v1.exceptions import (
    ApiTypeError,
    ApiValueError
)


class ServeApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def deploy_server(self, endpoint_id, project_id, **kwargs):  # noqa: E501
        """deploy_server  # noqa: E501

        Deploys a model server at given endpoint  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.deploy_server(endpoint_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str endpoint_id: The endpoint's public id (required)
        :param str project_id: Project ID of model server. (required)
        :param ModelServerSchema model_server_schema:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ModelServerSchema
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.deploy_server_with_http_info(endpoint_id, project_id, **kwargs)  # noqa: E501

    def deploy_server_with_http_info(self, endpoint_id, project_id, **kwargs):  # noqa: E501
        """deploy_server  # noqa: E501

        Deploys a model server at given endpoint  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.deploy_server_with_http_info(endpoint_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str endpoint_id: The endpoint's public id (required)
        :param str project_id: Project ID of model server. (required)
        :param ModelServerSchema model_server_schema:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ModelServerSchema, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['endpoint_id', 'project_id', 'model_server_schema']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method deploy_server" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'endpoint_id' is set
        if ('endpoint_id' not in local_var_params or
                local_var_params['endpoint_id'] is None):
            raise ApiValueError("Missing the required parameter `endpoint_id` when calling `deploy_server`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in local_var_params or
                local_var_params['project_id'] is None):
            raise ApiValueError("Missing the required parameter `project_id` when calling `deploy_server`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'endpoint_id' in local_var_params:
            path_params['endpoint_id'] = local_var_params['endpoint_id']  # noqa: E501

        query_params = []
        if 'project_id' in local_var_params:
            query_params.append(('project_id', local_var_params['project_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'model_server_schema' in local_var_params:
            body_params = local_var_params['model_server_schema']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['AccessTokenAuth', 'BearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/endpoint/{endpoint_id}/server/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ModelServerSchema',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_endpoint(self, endpoint_id, project_id, **kwargs):  # noqa: E501
        """get_endpoint  # noqa: E501

        Get a model endpoint  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_endpoint(endpoint_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str endpoint_id: Endpoint ID (required)
        :param str project_id: Project ID to create under. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ModelEndpointSchema
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_endpoint_with_http_info(endpoint_id, project_id, **kwargs)  # noqa: E501

    def get_endpoint_with_http_info(self, endpoint_id, project_id, **kwargs):  # noqa: E501
        """get_endpoint  # noqa: E501

        Get a model endpoint  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_endpoint_with_http_info(endpoint_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str endpoint_id: Endpoint ID (required)
        :param str project_id: Project ID to create under. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ModelEndpointSchema, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['endpoint_id', 'project_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_endpoint" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'endpoint_id' is set
        if ('endpoint_id' not in local_var_params or
                local_var_params['endpoint_id'] is None):
            raise ApiValueError("Missing the required parameter `endpoint_id` when calling `get_endpoint`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in local_var_params or
                local_var_params['project_id'] is None):
            raise ApiValueError("Missing the required parameter `project_id` when calling `get_endpoint`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'endpoint_id' in local_var_params:
            path_params['endpoint_id'] = local_var_params['endpoint_id']  # noqa: E501

        query_params = []
        if 'project_id' in local_var_params:
            query_params.append(('project_id', local_var_params['project_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['AccessTokenAuth', 'BearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/endpoint/{endpoint_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ModelEndpointSchema',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_model_server_image_path(self, endpoint_id, server_id, project_id, **kwargs):  # noqa: E501
        """get_model_server_image_path  # noqa: E501

        Get the path of the image baked for a model server deployed to an endpoint.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_model_server_image_path(endpoint_id, server_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str endpoint_id: The endpoint's public ID (required)
        :param str server_id: The server's public ID (required)
        :param str project_id: Project ID. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_model_server_image_path_with_http_info(endpoint_id, server_id, project_id, **kwargs)  # noqa: E501

    def get_model_server_image_path_with_http_info(self, endpoint_id, server_id, project_id, **kwargs):  # noqa: E501
        """get_model_server_image_path  # noqa: E501

        Get the path of the image baked for a model server deployed to an endpoint.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_model_server_image_path_with_http_info(endpoint_id, server_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str endpoint_id: The endpoint's public ID (required)
        :param str server_id: The server's public ID (required)
        :param str project_id: Project ID. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(str, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['endpoint_id', 'server_id', 'project_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_model_server_image_path" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'endpoint_id' is set
        if ('endpoint_id' not in local_var_params or
                local_var_params['endpoint_id'] is None):
            raise ApiValueError("Missing the required parameter `endpoint_id` when calling `get_model_server_image_path`")  # noqa: E501
        # verify the required parameter 'server_id' is set
        if ('server_id' not in local_var_params or
                local_var_params['server_id'] is None):
            raise ApiValueError("Missing the required parameter `server_id` when calling `get_model_server_image_path`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in local_var_params or
                local_var_params['project_id'] is None):
            raise ApiValueError("Missing the required parameter `project_id` when calling `get_model_server_image_path`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'endpoint_id' in local_var_params:
            path_params['endpoint_id'] = local_var_params['endpoint_id']  # noqa: E501
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']  # noqa: E501

        query_params = []
        if 'project_id' in local_var_params:
            query_params.append(('project_id', local_var_params['project_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain'])  # noqa: E501

        # Authentication setting
        auth_settings = ['AccessTokenAuth', 'BearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/endpoint/{endpoint_id}/server/{server_id}/image', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def undeploy_server(self, endpoint_id, server_id, project_id, **kwargs):  # noqa: E501
        """undeploy_server  # noqa: E501

        Undeploys a specific model server on an endpoint. The endpoint remains intact.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.undeploy_server(endpoint_id, server_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str endpoint_id: Endpoint ID (required)
        :param str server_id: Server ID (required)
        :param str project_id: Project ID. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ModelServerSchema
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.undeploy_server_with_http_info(endpoint_id, server_id, project_id, **kwargs)  # noqa: E501

    def undeploy_server_with_http_info(self, endpoint_id, server_id, project_id, **kwargs):  # noqa: E501
        """undeploy_server  # noqa: E501

        Undeploys a specific model server on an endpoint. The endpoint remains intact.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.undeploy_server_with_http_info(endpoint_id, server_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str endpoint_id: Endpoint ID (required)
        :param str server_id: Server ID (required)
        :param str project_id: Project ID. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ModelServerSchema, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['endpoint_id', 'server_id', 'project_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method undeploy_server" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'endpoint_id' is set
        if ('endpoint_id' not in local_var_params or
                local_var_params['endpoint_id'] is None):
            raise ApiValueError("Missing the required parameter `endpoint_id` when calling `undeploy_server`")  # noqa: E501
        # verify the required parameter 'server_id' is set
        if ('server_id' not in local_var_params or
                local_var_params['server_id'] is None):
            raise ApiValueError("Missing the required parameter `server_id` when calling `undeploy_server`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in local_var_params or
                local_var_params['project_id'] is None):
            raise ApiValueError("Missing the required parameter `project_id` when calling `undeploy_server`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'endpoint_id' in local_var_params:
            path_params['endpoint_id'] = local_var_params['endpoint_id']  # noqa: E501
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']  # noqa: E501

        query_params = []
        if 'project_id' in local_var_params:
            query_params.append(('project_id', local_var_params['project_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['AccessTokenAuth', 'BearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/endpoint/{endpoint_id}/server/{server_id}/undeploy', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ModelServerSchema',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
