import os
from typing import Optional
from enum import Enum
import humps
from pydantic import BaseModel  # pylint: disable=no-name-in-module

BALENA_PREFIX = 'BALENA' if os.getenv('BALENA') else 'RESIN' if os.getenv('RESIN') else 'DEBUG'
CUR_DIR = os.path.dirname(os.path.realpath(__file__))

class CamelModel(BaseModel):
    class Config:
        alias_generator = humps.camelize
        allow_population_by_field_name = True

class AppDataV1(BaseModel):
    type: str
    port: int

class TextResponseEnum(str, Enum):
    Success = 'Success'
    Failure = 'Failure'
    @classmethod
    def from_bool(cls, success: bool):
        return cls.Success if success else cls.Failure

class WifiMode(str, Enum):
    HOTSPOT = 'HOTSPOT'
    CLIENT = 'CLIENT'
    DISABLED = 'DISABLED'

class ContainerStates(str, Enum):
    EXITED = 'EXITED'
    DOWNLOADING = 'DOWNLOADING'
    DOWNLOADED = 'DOWNLOADED'
    INSTALLING = 'INSTALLING'
    INSTALLED = 'INSTALLED'
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    STOPPING = 'STOPPING'
    STOPPED = 'STOPPED'

class NetworkCredentials(CamelModel):
    mode: Optional[WifiMode] = None
    ssid: Optional[str] = None
    passphrase: Optional[str] = None
    identity: Optional[str] = None
    iface: Optional[str] = None

class NetworkCredentialCleaned(CamelModel):
    mode: Optional[WifiMode] = None
    ssid: Optional[str] = None
    identity: Optional[str] = None
    iface: Optional[str] = None

class BalenaSupervisor(CamelModel):
    version: str = os.getenv(f'{BALENA_PREFIX}_SUPERVISOR_VERSION', '0.0.0')
    address: str = os.getenv(f'{BALENA_PREFIX}_SUPERVISOR_ADDRESS', 'http://localhost:48484')
    api_key: str = os.getenv(f'{BALENA_PREFIX}_SUPERVISOR_API_KEY', '')


class AppInfo(CamelModel):
    id: int = int(os.getenv(f'{BALENA_PREFIX}_APP_ID', '0'))
    name: str = os.getenv(f'{BALENA_PREFIX}_APP_NAME', 'App')
    version: str = os.getenv('APP_VERSION', '0.0.0')
    commit: str = ''
    log_path: str = os.getenv('APP_LOG_PATH', '/tmp/logs')
    web_port: int = int(os.getenv('APP_WEB_PORT', '80'))
    img_path: str = os.getenv('APP_IMG_PATH', os.path.join(CUR_DIR, '../static/img.png'))

    img: bytes = b''
    status: str = 'IDLE'
    update_download_progress: int = 0
    update_available: bool = False
    update_downloading: bool = False
    update_installing: bool = False


class DeviceInfo(CamelModel):
    id: str = os.getenv(f'{BALENA_PREFIX}_DEVICE_UUID', '0000000')
    name: str = os.getenv(f'{BALENA_PREFIX}_DEVICE_NAME_AT_INIT', '')
    type: str = os.getenv(f'{BALENA_PREFIX}_DEVICE_TYPE', 'raspberrypi3')
    ip_address: str = ''


class DeviceState(CamelModel):
    status: str = 'IDLE'
    app_commit: str = ''
    app_version: str = '0.0.0'
    app_download_progress: int = 0
    app_update_available: bool = False
    app_downloading: bool = False
    app_updating: bool = False
    app_update_check: bool = False
    ip_address: str = ''
    device_UUID: str = ''
    device_name: str = ''
    internet_access: bool = False
    ap_mode: bool = False


class SDCSettings(CamelModel):
    wifi = NetworkCredentials(
        mode=WifiMode(os.getenv('SDC_WIFI_TYPE', 'HOTSPOT').upper()),
        ssid=os.getenv('SDC_WIFI_SSID', 'SDC-'+os.getenv(f'{BALENA_PREFIX}_DEVICE_UUID', '0000000')[:7]),
        passphrase=os.getenv('SDC_WIFI_PASS', 'samtec1!'),
        identity=None,
        iface=os.getenv('SDC_WIFI_IFACE', 'wlan0')
    )
