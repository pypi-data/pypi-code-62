import os
import tempfile
from asyncio import CancelledError, shield
from typing import Optional
import uvicorn
from fastapi import FastAPI, status, HTTPException, Body
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import samtecdeviceshare
from samtecdeviceshare.types import DeviceState, NetworkCredentialCleaned, NetworkCredentials, AppDataV1, TextResponseEnum
from samtecdeviceshare.logger import setup_logger
from samtecdeviceshare.sdshare import SamtecDeviceShare

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

logger = setup_logger('samtecdeviceshare', os.getenv('APP_LOG_PATH', tempfile.gettempdir()))
sds = SamtecDeviceShare()
app = FastAPI(
    title='Samtec Device Share',
    version=samtecdeviceshare.__version__
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info('Server starting up')
    await sds.open()

@app.on_event("shutdown")
async def shutdown_event():
    logger.warning('Server shutting down')
    await sds.close()

#######################################################################################################################
# REST Routes (v1 - legacy)
#######################################################################################################################

@app.get("/data.json", response_model=AppDataV1, status_code=status.HTTP_200_OK, description='''
Get minimal device information including type and web port. ''')
async def get_app_data():
    return AppDataV1(type=sds.app_info.name, port=sds.app_info.web_port)

@app.get("/img.png", description='''
Get app icon.''')
async def get_app_img() -> bytes:
    return Response(content=sds.app_info.img, media_type="application/octet-stream", status_code=status.HTTP_200_OK)

#######################################################################################################################
# REST Routes (v2)
#######################################################################################################################

@app.get("/api/v2/device", response_model=DeviceState, status_code=status.HTTP_200_OK, description='''
Get full device information.''')
async def get_device_state():
    return await sds.get_device_state()

@app.get("/api/v2/app", status_code=status.HTTP_200_OK, description='''
Get full app and services information.''')
async def get_app_state():
    try:
        return await sds.get_supervisor_app_state()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to get app state w/ error: {0}'.format(err))

@app.get("/api/v2/app/logs", description='Download all app logs as a zip.')
async def get_app_logs() -> bytes:
    try:
        log_data = await sds.get_log_zip_data()
        return Response(content=log_data, media_type="application/octet-stream", status_code=status.HTTP_200_OK)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to get app logs w/ error: {0}'.format(err))

@app.get('/api/v2/network/wifi/credentials', response_model=NetworkCredentialCleaned, status_code=status.HTTP_200_OK, description='''
Get WiFi connection information. __NOTE__: Only gets stored default connection for now.''')
async def get_wifi_network():
    ''' TODO: This just returns the default WiFi credentials and not actively set.'''
    return sds.settings.wifi

@app.post('/api/v2/device/blink', status_code=status.HTTP_200_OK, description='''
Have the device blink for 15 seconds.''')
async def blink_device() -> TextResponseEnum:
    try:
        success = await sds.blink_device()
        return TextResponseEnum.from_bool(success)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to get app state w/ error: {0}'.format(err))


@app.post('/api/v2/device/restart', status_code=status.HTTP_202_ACCEPTED, description='''
Performs a full reboot of the device.''')
async def restart_device() -> TextResponseEnum:
    success = await sds.restart_app()
    return TextResponseEnum.from_bool(success)

@app.post('/api/v2/app/update/check', status_code=status.HTTP_204_NO_CONTENT, description='''
Checks if an app update exists and if so downloads it. ''')
async def app_update_check(credentials: Optional[NetworkCredentials] = Body(default=None)) -> TextResponseEnum:
    try:
        await shield(sds.perform_ota_update_check(credentials))
        return TextResponseEnum.Success
    except (CancelledError, ConnectionResetError) as err:
        logger.exception('Request cancelled or reset (error: %s)', err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to perform update check w/ error: {0}'.format(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to perform update check w/ error: {0}'.format(err))

@app.post('/api/v2/app/update/install', status_code=status.HTTP_204_NO_CONTENT, description='''
Installs update if downloaded and restarts app.''')
async def app_update_install() -> TextResponseEnum:
    try:
        await sds.update_app()
        return TextResponseEnum.Success
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to perform update w/ error: {0}'.format(err))

@app.post('/api/v2/network/wifi/credentials', status_code=status.HTTP_200_OK, description='''
Temporarily connect to supplied WiFi network. Connection is cleared on reboot or app restart.''')
async def set_wifi_network(credentials: Optional[NetworkCredentials] = Body(default=None)) -> TextResponseEnum:
    try:
        await sds.launch_wifi_client(credentials)
        return TextResponseEnum.Success
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to update WiFi credentials w/ error: {0}'.format(err))

@app.post('/api/v2/network/wifi/hotspot', status_code=status.HTTP_200_OK, description='''
Force device to temporarily launch WiFi hotspot. Connection is cleared on reboot or app restart.''')
async def set_wifi_hotspot(credentials: Optional[NetworkCredentials] = Body(default=None))-> TextResponseEnum:
    try:
        await sds.launch_hot_spot(credentials)
        return TextResponseEnum.Success
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to update WiFi credentials w/ error: {0}'.format(err))

#######################################################################################################################
# REST Routes (v2)
#######################################################################################################################

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('REST_ADDRESS', '0.0.0.0'), port=int(os.getenv('REST_PORT', '47546')))
