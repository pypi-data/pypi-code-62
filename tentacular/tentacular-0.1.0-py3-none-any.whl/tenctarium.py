import inspect
import traceback
import uvicorn
import json

from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/{endpoint}/{uid}')
class DeviceEndpoint(HTTPEndpoint):

    @staticmethod
    async def _call_function(func, data, endpoint, uid):
        if inspect.iscoroutinefunction(func):
            await func(data, endpoint, uid)
        else:
            func(data, endpoint, uid)

    async def post(self, request):

        data = await request.body()
        if data:
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                return JSONResponse(
                    {'message': f'Failed to read data:{e}'},
                    status_code=400
                )

        endpoint = request.path_params['endpoint']
        uid = request.path_params['uid']

        if not endpoint in DeviceCallback.instances:
            return JSONResponse(
                {'message':f'Endpoint {endpoint} is not available'},
                status_code=400
            )

        try:
            request_validator = DeviceCallback.instances[endpoint].request_validator
            if request_validator is not None:
                request_validator.validate()
        except Exception as e:
            return JSONResponse(
                {'message':f'Validation failed:\n{e}'},
                status_code=400
            )
    
        callback_func = DeviceCallback.instances[endpoint].callback_func

        try:
            await self._call_function(
                    callback_func,
                    data=data,
                    endpoint=endpoint,
                    uid=uid
            )
            return JSONResponse({'message':'Success'}, status_code=200)
        except BaseException:
            traceback.print_exc()
            return JSONResponse(
                {'message':'Callback failed'},
                status_code=500
            )


class DeviceCallback:
    instances = {}

    def __init__(self, endpoint, callback_func, request_validator=None):
        self.endpoint = endpoint
        self.callback_func = callback_func
        self.request_validator = request_validator
        DeviceCallback.instances[self.endpoint] = self

class device_callback:
    def __init__(self, endpoint, request_validator=None):
        self.endpoint = endpoint
        self.request_validator = request_validator


    def __call__(self, fn):
        DeviceCallback(
            endpoint=self.endpoint, 
            callback_func=fn,
            request_validator=self.request_validator
        )
        return fn

def tenctarium(host='localhost', port=8090):
    uvicorn.run(app, host=host, port=port)