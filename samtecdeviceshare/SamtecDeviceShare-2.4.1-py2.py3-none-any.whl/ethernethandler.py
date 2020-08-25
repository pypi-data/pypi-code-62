""" Ethernet Handler """
#!/usr/bin/env python
import os
import time
import tempfile
from samtecdeviceshare.helper import env_flag
from samtecdeviceshare.logger import setup_logger

logger = setup_logger('samtecdeviceshare', os.getenv('APP_LOG_PATH', tempfile.gettempdir()))

try:
    import NetworkManager as NM  # type: ignore
except Exception as err:
    if os.getenv('PYTHON_ENV') == 'development':
        logger.warning('Failed to load NetworkManager. Using emulator in development.')
    else:
        logger.warning('Failed to load NetworkManager module.')
    class NetworkManager:
        @classmethod
        def GetDevices(cls):
            return []
        ActiveConnections = []
        @classmethod
        def ActivateConnection(cls, *args, **kwargs):
            pass
    class NetworkManagerModule:
        NM_DEVICE_STATE_ACTIVATED = 100
        NM_DEVICE_STATE_IP_CHECK = 80
        NM_DEVICE_STATE_IP_CONFIG = 70
        NM_DEVICE_STATE_FAILED = 120
        NM_DEVICE_STATE_UNAVAILABLE = 20
        NM_DEVICE_STATE_UNMANAGED = 10
        NM_DEVICE_TYPE_ETHERNET = 1
        NetworkManager = NetworkManager
        @classmethod
        def nm_state(cls):
            pass
    NM = NetworkManagerModule

class EthernetHandler:
    CONN_STATES = ['DISCONNECTED', 'CONNECTING', 'CONNECTED']
    NM_CONNECTED_STATES = [NM.NM_DEVICE_STATE_ACTIVATED]
    NM_CONNECTING_STATES = [
        NM.NM_DEVICE_STATE_IP_CHECK,
        NM.NM_DEVICE_STATE_IP_CONFIG
    ]
    NM_DISCONNECTED_STATES = [
        NM.NM_DEVICE_STATE_FAILED,
        NM.NM_DEVICE_STATE_UNAVAILABLE,
        NM.NM_DEVICE_STATE_UNMANAGED
    ]

    def __init__(self, target_dev_name=None):
        self.DHCP_TIMEOUT = int(os.getenv('ETH_DHCP_TIMEOUT', '15'))
        self.LINK_LOCAL_TIMEOUT = int(os.getenv('ETH_LOCAL_TIMEOUT', '30'))
        self.target_dev_name = target_dev_name or os.getenv('ETH_TARGET_NAME')
        self.REFRESH_DELAY = 1
        self.dev_name = None
        self.dev_state = None
        self.con_name = None
        self.con_state = 'DISCONNECTED'
        self.con_counter = 0
        self.con_needs_init = True

    def run(self):
        while True:
            try:
                time.sleep(self.REFRESH_DELAY)
                self.update()
            except Exception as err:
                logger.exception('Received following exception: %s', err)

    def getWiredDevice(self):
        for dev in NM.NetworkManager.GetDevices():
            is_ethernet = dev.DeviceType == NM.NM_DEVICE_TYPE_ETHERNET
            is_target_device = not self.target_dev_name or (self.target_dev_name and self.target_dev_name == dev.Interface)
            if is_ethernet and is_target_device:
                return dev
        return None

    def getActiveWiredConnection(self):
        for act in NM.NetworkManager.ActiveConnections:
            try:
                settings = act.Connection.GetSettings()
                act_devs = act.Devices
                # Skip if connection isnt 802-3-ethernet or no devices attached
                if settings['connection'].get('type') != '802-3-ethernet' or '802-3-ethernet' not in settings or not act_devs:
                    continue
                # If no target specified, pick first dev
                if not self.target_dev_name:
                    return act.Connection, act_devs[0]
                # Otherwise, find target device
                foundDev = next((d for d in act_devs if d.Interface == self.target_dev_name), None)
                if foundDev:
                    return act.Connection, foundDev
            except Exception as err:
                logger.warning('Skipping active connection. Failed parsing with error: %s', err)
        return None, None

    def updateActiveWiredConnection(self, con=None, dev=None, method='auto'):
        success = False
        try:
            settings = con.GetSettings()
            # Add IPv4 setting if it doesn't yet exist
            if 'ipv4' not in settings:
                settings['ipv4'] = {}
            # Set the method and change properties
            settings['ipv4']['method'] = method
            settings['ipv4']['addresses'] = []
            con.Update(settings)
            con.Save()
            NM.NetworkManager.ActivateConnection(con, dev, "/")
            success = True
        except Exception:
            success = False
        return success

    def update(self):
        if os.getenv('PYTHON_ENV') == 'development':
            return
        # Disable this feature (e.g pi zero)
        if env_flag('ETH_DISABLE', False):
            return
        next_con_name = None
        next_dev_name = None
        next_dev_state = None
        next_con_method = None
        next_con_state = None
        con, dev = self.getActiveWiredConnection()

        # Get device and connection name and state
        if con is None or dev is None:
            self.con_needs_init = True
            dev = self.getWiredDevice()
            con_settings = None
            con_method = 'auto'
            next_con_name = 'Unknown'
            next_dev_name = dev.Interface if dev else None
            next_dev_state = dev.State if dev else NM.NM_DEVICE_STATE_UNAVAILABLE
        else:
            con_settings = con.GetSettings()
            con_method = con_settings.get('ipv4', {}).get('method', '')
            next_con_name = con_settings.get('connection', {}).get('id', '')
            next_dev_name = dev.Interface
            next_dev_state = dev.State

        # Determine whether to change connection method
        if next_dev_state in EthernetHandler.NM_CONNECTED_STATES:
            self.con_counter = 0
            next_con_state = 'CONNECTED'
            next_con_method = con_method
        elif next_dev_state in EthernetHandler.NM_CONNECTING_STATES:
            next_con_state = 'CONNECTING'
            # DHCP timeout, go to Link-Local
            if con_method == 'auto' and self.con_counter >= self.DHCP_TIMEOUT:
                logger.info('auto method timeout. Switching to link-local')
                next_con_method = 'link-local'
                self.con_counter = 0
            # Link-Local timeout, go to DHCP
            elif con_method == 'link-local' and self.con_counter >= self.LINK_LOCAL_TIMEOUT:
                logger.info('link-local method timeout. Switching to auto')
                next_con_method = 'auto'
                self.con_counter = 0
            else:
                next_con_method = con_method
                self.con_counter += 1

        elif next_dev_state in EthernetHandler.NM_DISCONNECTED_STATES:
            self.con_counter = 0
            next_con_state = 'DISCONNECTED'
            next_con_method = 'auto'
        else:
            self.con_counter = self.con_counter
            next_con_method = con_method

        if next_dev_name != self.dev_name:
            logger.info('Wired device name changed to {0}'.format(next_dev_name))
        if next_con_name != self.con_name:
            logger.info('Wired connection name changed to {0}'.format(next_con_name))
        if next_con_state != self.con_state:
            logger.info('Wired connection state changed to {0}'.format(next_con_state))

        # If have connection and want method to change or needs initialization
        if con and (self.con_needs_init or (next_con_method != con_method)):
            # IMPORTANT: On init we must start with DHCP
            next_con_method = 'auto' if self.con_needs_init else next_con_method
            logger.info('Setting connection {0} to method {1}'.format(next_con_name, next_con_method))
            success = self.updateActiveWiredConnection(con, dev, next_con_method)
            # NOTE: If failed to activate, we'll retry next iteration
            if not success:
                next_con_method = con_method
                self.con_needs_init = True
                logger.error('Failed setting active connection method.')
            else:
                self.con_needs_init = False
                logger.info('Successfully set active connection method.')
        self.dev_name = next_dev_name
        self.dev_state = next_dev_state
        self.con_name = next_con_name
        self.con_state = next_con_state

if __name__ == '__main__':
    handler = EthernetHandler()
    handler.run()
