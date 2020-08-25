#!/usr/bin/env python
import os
import socket
import uuid
import time
import struct
import functools
import fcntl
import tempfile
import asyncio
from concurrent.futures import Executor
from typing import List, Any, Optional, Callable
from uuid import UUID
from samtecdeviceshare.logger import setup_logger
from samtecdeviceshare.types import NetworkCredentials

logger = setup_logger('samtecdeviceshare', os.getenv('APP_LOG_PATH', tempfile.gettempdir()))

try:
    import dbus  # type: ignore
except Exception as err:
    dbus = None
    if os.getenv('PYTHON_ENV') == 'development':
        logger.warning('Failed to load dbus module. Using emulator in development.')
    else:
        logger.warning('Failed to load dbus module.')

def is_online(host="8.8.8.8", port=53, timeout=3) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def env_flag(env_var: str, default: bool = False) -> bool:
    """
    Return the specified environment variable coerced to a bool, as follows:
    - When the variable is unset, or set to the empty string, return `default`.
    - When the variable is set to a truthy value, returns `True`.
      These are the truthy values:
          - 1
          - true, yes, on
    - When the variable is set to the anything else, returns False.
       Example falsy values:
          - 0
          - no
    - Ignore case and leading/trailing whitespace.
    """
    environ_string = os.environ.get(env_var, "").strip().lower()
    if not environ_string:
        return default
    return environ_string in ["1", "true", "yes", "on"]

def is_on_balena() -> bool:
    return bool(os.getenv('BALENA') or os.getenv('RESIN'))

def valid_wpa_passphrase(passphrase: Any) -> bool:
    if passphrase is None:
        return True
    if not isinstance(passphrase, str):
        return False
    return len(passphrase) >= 8 and len(passphrase) <= 63

def get_ip_address(ifname: str):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except Exception:
        return ''

def get_ip_addresses() -> List[str]:
    ''' Get all IPv4 addresses using active connections via dbus. NOTE: This can include local networks such as Docker.'''
    if os.getenv('PYTHON_ENV') == 'development' or dbus is None:
        return []
    # Require access to system bus
    bus = dbus.SystemBus()
    # Access network manager (nm)
    nm = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
    # Get active connections
    conn_paths = nm.Get("org.freedesktop.NetworkManager", "ActiveConnections", dbus_interface=dbus.PROPERTIES_IFACE)
    ip_addesses: List[str] = []
    for conn_path in conn_paths:
        conn = bus.get_object("org.freedesktop.NetworkManager", conn_path)
        ipv4_config_path = conn.Get("org.freedesktop.NetworkManager.Connection.Active", "Ip4Config", dbus_interface=dbus.PROPERTIES_IFACE)
        ipv4_config = bus.get_object("org.freedesktop.NetworkManager", ipv4_config_path)
        address_data = ipv4_config.Get("org.freedesktop.NetworkManager.IP4Config", "AddressData", dbus_interface=dbus.PROPERTIES_IFACE)
        for address in address_data:
            ip_addesses.append(str(address["address"]))
    return ip_addesses

async def awaitify(loop: Optional[asyncio.AbstractEventLoop] = None, pool: Optional[Executor] = None, func: Optional[Callable] = None, **kwargs):
    if func is None:
        return
    if loop is None:
        loop = asyncio.get_running_loop()
    routine = functools.partial(func, **kwargs)
    rsts = await loop.run_in_executor(pool, routine)
    return rsts

def setup_wifi_hotspot(credentials: NetworkCredentials, con_uuid: Optional[UUID] = None, action: Optional[str] = None, timeout: float = 10):
    if os.getenv('PYTHON_ENV') == 'development' or dbus is None:
        print('Creating wifi hotspot {credentials.ssid} on iface {credentials.iface}')
        return
    ssid_bytes = dbus.ByteArray(credentials.ssid.encode("utf-8"))
    # If id is matched in setup_wifi_connection the UUID is replaced with previous
    wifi_uuid = con_uuid if con_uuid else str(uuid.uuid4())
    # wifi_uuid = con_uuid if con_uuid else '0cd1611e-942c-48b0-aa49-756a6a3818b7'
    wifi_channel = dbus.UInt32(1)
    s_con = dbus.Dictionary(dict(type='802-11-wireless', uuid=wifi_uuid, id=credentials.ssid))
    s_wifi = dbus.Dictionary(dict(ssid=ssid_bytes, mode='ap', band='bg', channel=wifi_channel))
    if credentials.passphrase:
        s_wsec = dbus.Dictionary({'key-mgmt': 'wpa-psk', 'proto': ['rsn'], 'psk': credentials.passphrase})
    else:
        s_wsec = dbus.Dictionary({'key-mgmt': 'none', 'auth-alg': 'open'})
    s_ip4 = dbus.Dictionary(dict(method='shared'))
    s_ip6 = dbus.Dictionary(dict(method='ignore'))
    con = dbus.Dictionary({
        'connection': s_con,
        '802-11-wireless': s_wifi,
        '802-11-wireless-security': s_wsec,
        'ipv4': s_ip4,
        'ipv6': s_ip6
    })
    setup_wifi_connection(con, iface=credentials.iface, action=action, timeout=timeout)

# pylint: disable=too-many-arguments,too-many-locals
def setup_wifi_client(credentials: NetworkCredentials, con_uuid=None, action=None, timeout=10):
    if os.environ.get('PYTHON_ENV') == 'development' or dbus is None:
        print(f'Creating wifi client {credentials.ssid} {credentials.passphrase} on iface {credentials.iface}')
        return
    ssid_bytes = dbus.ByteArray(credentials.ssid.encode("utf-8"))
    # If id is matched in setupWIFIConnection the UUID is replaced with previous
    wifi_uuid = con_uuid if con_uuid else str(uuid.uuid4())
    s_con = dbus.Dictionary(dict(type='802-11-wireless', uuid=wifi_uuid, id=credentials.ssid))
    s_wifi = dbus.Dictionary(dict(ssid=ssid_bytes, security='802-11-wireless-security'))
    # WPA2 Enterprise
    if isinstance(credentials.identity, str) and len(credentials.identity) > 1:
        s_wsec = dbus.Dictionary({'key-mgmt': 'wpa-eap', 'auth-alg': 'open'})
        s_eap = dbus.Dictionary({
            'eap': 'peap',
            'identity': credentials.identity,
            'phase2-auth': 'mschapv2',
            'password': credentials.passphrase
        })
    # WPA2 Regular
    elif credentials.passphrase:
        s_wsec = dbus.Dictionary({'key-mgmt': 'wpa-psk', 'psk': credentials.passphrase, 'auth-alg': 'open'})
        s_eap = None
    # WEP open
    else:
        s_wsec = dbus.Dictionary({'key-mgmt': 'none', 'auth-alg': 'open'})
        s_eap = None

    s_ip4 = dbus.Dictionary({'method': 'auto'})
    s_ip6 = dbus.Dictionary({'method': 'auto'})
    con = dbus.Dictionary({
        'connection': s_con,
        '802-11-wireless': s_wifi,
        '802-11-wireless-security': s_wsec,
        'ipv4': s_ip4,
        'ipv6': s_ip6
    })
    if s_eap:
        con.update(dbus.Dictionary({'802-1x': s_eap}))
    setup_wifi_connection(con, iface=credentials.iface, action=action, timeout=timeout)

def setup_wifi_connection(con, iface='wlan0', action=None, timeout=10):
    try:
        if os.getenv('PYTHON_ENV') == 'development' or dbus is None:
            print(f'Creating wifi connection on iface {iface}')
            return
        bus = dbus.SystemBus()
        service_name = "org.freedesktop.NetworkManager"
        proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager/Settings")
        settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

        proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager")
        nm = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
        dev_path = nm.GetDeviceByIpIface(iface)

        # Find our existing connection
        con_path = None
        con_settings = None
        config = None
        for path in settings.ListConnections():
            proxy = bus.get_object(service_name, path)
            con_settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings.Connection")
            config = con_settings.GetSettings()
            if config['connection']['id'] == con['connection']['id']:
                con_path = path
                break

        # If connection already exist, update it
        if con_path:
            con['connection']['uuid'] = config['connection']['uuid']
            con_settings.Update(con)
            con_settings.Save()
        # If connection doesnt exist, add it
        else:
            con_path = settings.AddConnection(con)

        # If no action, return
        if action is None:
            return

        # Now start or stop the connection on the requested device
        proxy = bus.get_object(service_name, dev_path)
        device = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Device")
        if str(action).upper() == 'UP':
            act_path = nm.ActivateConnection(con_path, dev_path, "/")
            proxy = bus.get_object(service_name, act_path)
            act_props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
            time.sleep(0.5)
            # Wait for the connection to start up
            start = time.time()
            while time.time() < start + int(timeout):
                state = act_props.Get("org.freedesktop.NetworkManager.Connection.Active", "State")
                if state == 2:  # NM_ACTIVE_CONNECTION_STATE_ACTIVATED
                    return
                time.sleep(1)
            raise Exception('Failed to start wifi connection due to timeout')
        if str(action).upper() == 'DOWN':
            device.Disconnect()
            return
        raise Exception('Unsupported action')
    except Exception as err:
        raise err


if __name__ == "__main__":
    pass
