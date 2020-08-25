import os
import time
import glob
import tempfile
import zipfile
from typing import Optional
import asyncio
from asyncio import CancelledError, shield
from concurrent.futures import ThreadPoolExecutor
import lockfile
from lockfile import LockFile
import aiohttp
from samtecdeviceshare.types import AppInfo, DeviceInfo, DeviceState, BalenaSupervisor, SDCSettings, WifiMode, NetworkCredentials, BALENA_PREFIX
from samtecdeviceshare.helper import is_online, get_ip_address, setup_wifi_hotspot, setup_wifi_client, awaitify, valid_wpa_passphrase
from samtecdeviceshare.ethernethandler import EthernetHandler
from samtecdeviceshare.logger import setup_logger

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
logger = setup_logger('samtecdeviceshare', os.getenv('APP_LOG_PATH', tempfile.gettempdir()))


class SamtecDeviceShare:
    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.supervisor: BalenaSupervisor = BalenaSupervisor()
        self.app_info: AppInfo = AppInfo()
        self.device_info: DeviceInfo = DeviceInfo()
        self.settings = SDCSettings()
        lock_path = os.getenv(f'{BALENA_PREFIX}_APP_LOCK_PATH', '/tmp/balena.lock')
        if not os.path.exists(os.path.dirname(lock_path)):
            os.makedirs(os.path.dirname(lock_path))
        self.lock_handler = LockFile(os.path.splitext(lock_path)[0])
        self.ethernet_handler = EthernetHandler()
        self.internet_access = False
        self.__fetch: Optional[aiohttp.ClientSession] = None
        self.__background_task: Optional[asyncio.Task] = None
        self.__update_task: Optional[asyncio.Task] = None

    @property
    def balena_device(self) -> bool:
        return bool(os.getenv('BALENA') or os.getenv('RESIN'))

    @property
    def fetch(self) -> aiohttp.ClientSession:
        if self.__fetch is None or self.__fetch.closed:
            self.__fetch = aiohttp.ClientSession()
        return self.__fetch

    async def open(self) -> None:
        try:
            await self.check_internet_access()
            await self.set_app_lock(locked=True, timeout=5)
        except Exception as err:
            logger.exception('Failed acquiring lock w/ error: %s', err)
        try:
            await self.launch_default_wifi()
        except Exception as err:
            logger.exception('Failed launching WiFi w/ error: %s', err)
        try:
            with open(self.app_info.img_path, 'rb') as fp:
                self.app_info.img = fp.read()
        except Exception as err:
            logger.exception('Failed loading app image w/ error: %s', err)
        try:
            await self._update_device_state(force=True)
        except Exception as err:
            logger.exception('Failed updating device state w/ error: %s', err)
        self.__background_task = asyncio.create_task(self.update())

    async def close(self) -> None:
        if self.__background_task:
            self.__background_task.cancel()
            await self.__background_task
            self.__background_task = None
        if self.__fetch and not self.__fetch.closed:
            await self.__fetch.close()
            self.__fetch = None

    async def update(self) -> None:
        while True:
            try:
                for _ in range(3):
                    await asyncio.sleep(1)
                    await self._update_network_routine()
                await self._update_device_state()
                await self.check_internet_access()
            except CancelledError:
                logger.warning('Background task(s) cancelled')
                return
            except Exception as err:
                logger.exception('Failed performing update routine w/ error: %s', err)

    async def _update_network_routine(self) -> None:
        try:
            await awaitify(None, self.pool, self.ethernet_handler.update)
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed updating network due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed updating network w/ error: %s', err)
            raise err

    async def check_internet_access(self) -> bool:
        self.internet_access = await shield(awaitify(None, self.pool, is_online))
        return self.internet_access or False

    async def launch_default_wifi(self) -> None:
        if self.settings.wifi.mode == WifiMode.HOTSPOT:
            await self.launch_hot_spot(self.settings.wifi)
        elif self.settings.wifi.mode == WifiMode.CLIENT:
            await self.launch_wifi_client(self.settings.wifi)
        elif self.settings.wifi.mode == WifiMode.DISABLED:
            logger.debug('Wi-Fi is disabled')
        else:
            logger.warning('Invalid default Wi-Fi setup provided')

    async def launch_hot_spot(self, credentials: Optional[NetworkCredentials] = None):
        if credentials is None and self.settings.wifi.mode is not WifiMode.HOTSPOT:
            raise Exception('Unable to launch Wi-Fi Hotspot. No configuration defined.')
        if credentials is None or credentials.ssid is None:
            credentials = self.settings.wifi
        if credentials.iface is None:
            credentials.iface = self.settings.wifi.iface
        # Validate credentials
        if not isinstance(credentials.ssid, str):
            raise TypeError('Invalid wifi credentials: SSID missing or incorrect.')
        if not valid_wpa_passphrase(credentials.passphrase):
            raise TypeError('Invalid wifi credentials: Passphrase incorrect.')
        await shield(awaitify(
            None, self.pool, setup_wifi_hotspot, credentials=credentials, action='UP', timeout=20
        ))

    async def launch_wifi_client(self, credentials: Optional[NetworkCredentials] = None):
        if credentials is None and self.settings.wifi.mode is not WifiMode.CLIENT:
            raise Exception('Unable to launch Wi-Fi client. No configuration defined.')
        if credentials is None or credentials.ssid is None:
            credentials = self.settings.wifi
        if credentials.iface is None:
            credentials.iface = self.settings.wifi.iface
        # Validate credentials
        if not isinstance(credentials.ssid, str):
            raise TypeError('Invalid wifi credentials: SSID missing or incorrect.')
        if not valid_wpa_passphrase(credentials.passphrase):
            raise TypeError('Invalid wifi credentials: Passphrase incorrect.')
        await shield(awaitify(
            None, self.pool, setup_wifi_client,
            credentials=credentials, action='UP', timeout=20
        ))

    async def get_log_zip_data(self) -> bytes:
        data = await shield(awaitify(None, self.pool, self._zip_log_data))
        return data or bytes([])

    def _zip_log_data(self) -> bytes:
        zip_path = os.path.join(tempfile.gettempdir(), 'app_logs.zip')
        zip_fp = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        for log_file in glob.glob(os.path.join(self.app_info.log_path, '*.log')):
            zip_fp.write(log_file, f'app_logs/{os.path.basename(log_file)}')
        zip_fp.close()
        with open(zip_path, 'rb') as fp:
            data = fp.read()
        return data

    def set_lock_file(self, lock_handler, lock, timeout=5) -> None:
        if lock_handler is None:
            raise Exception('Invalid lock handler provided')
        if lock == lock_handler.is_locked():
            logger.warning('Lock file already set')
            return
        try:
            lock_handler.acquire(timeout=timeout) if lock else lock_handler.release()
        except lockfile.LockError as err:
            raise err
        except lockfile.UnlockError as err:
            logger.warning('Forcefully breaking lock file.')
            lock_handler.break_lock()
        logger.info("Lock file successfully %s.", 'locked' if lock else 'unlocked')

    async def set_app_lock(self, locked, timeout=5) -> None:
        if self.lock_handler:
            await shield(awaitify(
                None, self.pool, self.set_lock_file,
                lock_handler=self.lock_handler, lock=locked, timeout=timeout
            ))

    async def restart_app(self) -> bool:
        await self.set_app_lock(locked=False)
        uri = self.supervisor.address+'/v1/reboot'
        status = 400
        async with self.fetch.post(uri, params={'apikey': self.supervisor.api_key}) as resp:
            status = resp.status
        return status == 202

    async def update_app(self) -> bool:
        if self.app_info.update_installing:
            return True
        if self.app_info.update_downloading:
            raise Exception('App update still downloading')
        await self.supervisor_update_check(force=False)
        if not self.app_info.update_available:
            raise Exception('No app update available')
        # Remove update lock file
        await self.set_app_lock(locked=False)
        self.__update_task = asyncio.create_task(self.supervisor_update_check(force=True))
        return True

    async def blink_device(self) -> bool:
        uri = self.supervisor.address+'/v1/blink'
        status = 400
        async with self.fetch.post(uri, params={'apikey': self.supervisor.api_key}) as resp:
            status = resp.status
        return status == 200

    async def get_device_state(self) -> DeviceState:
        return DeviceState(
            status=self.app_info.status,
            app_commit=self.app_info.commit,
            app_version=self.app_info.version,
            app_download_progress=self.app_info.update_download_progress,
            app_update_available=self.app_info.update_available,
            app_downloading=self.app_info.update_downloading,
            app_updating=self.app_info.update_installing,
            app_update_check=self.__update_task is not None and not self.__update_task.done(),
            ip_address=self.device_info.ip_address,
            device_UUID=self.device_info.id,
            device_name=self.device_info.name,
            internet_access=self.internet_access,
            ap_mode='10.42.0.1' in self.device_info.ip_address
        )

    async def get_supervisor_device_state(self):
        uri = self.supervisor.address+'/v1/device'
        async with self.fetch.get(uri, params={'apikey': self.supervisor.api_key}) as resp:
            dev_state = await resp.json()
        return dev_state

    async def get_supervisor_app_state(self):
        uri = self.supervisor.address+'/v2/applications/state'
        async with self.fetch.get(uri, params={'apikey': self.supervisor.api_key}) as resp:
            app_state = await resp.json()
        return app_state

    async def supervisor_update_check(self, force=False) -> int:
        uri = self.supervisor.address+'/v1/update'
        params = {'apikey': self.supervisor.api_key}
        body = dict(force=force)
        status = 400
        async with self.fetch.post(uri, params=params, json=body) as resp:
            status = resp.status
        return status

    async def _update_device_state(self, force=False) -> None:
        app_commit = self.app_info.commit
        ifaces = [os.getenv('SDC_WIFI_IFACE', 'wlan0'), os.getenv('ETH_TARGET_NAME', 'eth0')]
        self.device_info.ip_address = ' '.join([get_ip_address(ifname) for ifname in ifaces])
        if self.balena_device and (self.internet_access or force):
            dev_state = await self.get_supervisor_device_state()
            app_state = await self.get_supervisor_app_state()
            app_commit = app_state.get(self.app_info.name, {}).get('commit', app_commit)
            services = app_state.get(self.app_info.name, {}).get('services', {}).values()
            service_statuses = [s.get('status', 'IDLE').upper() for s in services]

            # DOWNLOADING: At least 1 service is DOWNLOADING
            update_downloading = 'DOWNLOADING' in service_statuses
            update_download_progress = 0
            for service in services:
                if service.get('status', '').upper() == 'DOWNLOADING':
                    update_download_progress += service.get('downloadProgress', 0) or 0
                else:
                    update_download_progress += 100
            update_download_progress /= max(1, len(services))
            # UPDATE AVAILABLE: At least 1 service DOWNLOADED & rest either DOWNLOADED or RUNNING
            # NOTE: RUNNING is okay- Service could have previously downloaded/installed due to no lock (power cycle)
            # NOTE: Delta may fail messing up service state: DOWNLOADING > STOPPING > STARTING > RUNNING > DOWNLOADING
            update_available = 'DOWNLOADED' in service_statuses and all([s in ['DOWNLOADED', 'RUNNING'] for s in service_statuses])
            # UPDATE INSTALLING: At least 1 service INSTALLING & rest either INSTALLING, INSTALLED, STARTING, or RUNNING
            update_installing = 'INSTALLING' in service_statuses and all([s in ['INSTALLING', 'INSTALLED', 'STARTING', 'RUNNING'] for s in service_statuses])
            self.app_info.update_downloading = update_downloading
            self.app_info.update_download_progress = update_download_progress
            self.app_info.update_available = update_available
            self.app_info.update_installing = update_installing
        if self.balena_device and not app_commit and force:
            dev_state = await self.get_supervisor_device_state()
            app_commit = dev_state.get('commit', None)
        if app_commit is not None:
            self.app_info.commit = app_commit

    async def perform_ota_update_task(self, timeout=1800) -> None:
        try:
            # Trigger supervisor to check for an update
            logger.info('OTA Update Check: Started')
            await self._update_device_state()
            await asyncio.sleep(10)
            logger.info('OTA Update Check: Request update')
            await self.supervisor_update_check(force=False)
            await asyncio.sleep(20)
            app_downloading = True
            tic = time.time()
            while app_downloading:
                logger.info('OTA Update Check: Waiting for potential app update to complete')
                await self._update_device_state()
                app_downloading = self.app_info.update_downloading
                if time.time() - tic > timeout:
                    break
                await asyncio.sleep(10)
            logger.info('OTA Update Check: Finished')
            await self._update_device_state()
            await self.launch_default_wifi()
            return
        except Exception as err:
            logger.exception('OTA Update Check: Failed due to error: %s', err)
            await self.launch_default_wifi()

    async def perform_ota_update_check(self, credentials: Optional[NetworkCredentials]) -> None:
        try:
            if self.__update_task and not self.__update_task.done():
                return
            # Already online so just use it
            online = await self.check_internet_access()
            if online:
                await shield(self.supervisor_update_check(force=False))
                await asyncio.sleep(1)
                return

            # Connect to supplied network
            if credentials is None:
                raise Exception('No internet access and no/invalid Wi-Fi credentials provided.')
            await self.launch_wifi_client(credentials=credentials)
            # Wait 20 seconds for internet access
            num_attempts = 0
            online = False
            while num_attempts < 20 and not online:
                await asyncio.sleep(1)
                online = await self.check_internet_access()
                num_attempts += 1
            if not online:
                raise Exception('Timeout reached trying to contact server.')
            # Run in seperate task
            self.__update_task = asyncio.create_task(self.perform_ota_update_task())
            return
        except Exception as err:
            logger.exception('OTA Update Check: Failed due to error: %s', err)
            await self.launch_default_wifi()
            raise err
