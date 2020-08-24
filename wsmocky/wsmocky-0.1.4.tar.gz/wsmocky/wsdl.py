#coding=utf8

import requests
from lxml import etree
from io import StringIO, BytesIO

import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

def wsdl_from_url(url):
    """
    """
    if url.startswith('http'):
        return requests.get(url).text
    else:
        with open(url, 'r') as f:
            return f.read()


class Soap(object):
    def __init__(self, body):
        self.documents = etree.fromstring(body)

    def port_name(self):
        """获取Soap请求的接口"""
        for headerOrBody in self.documents:
            if headerOrBody.tag.endswith('Body'):
                for port in headerOrBody:
                    return port.tag.split('}')[-1]
        return ""


class WSDLService(object):
    def __init__(self, wsdl_text):
        self.documents = etree.fromstring(wsdl_text.encode('utf-8') if is_py3 else wsdl_text)
        self.location = ''
        self.portName = ''

    def bindings(self):
        """
        获取入口
        """
        for sub in self.documents:
            try:
                if sub.tag.endswith('service'):
                    service_root = sub
                    break
            except Exception as e:
                print(f'{e}')
        if service_root:
            for sub in service_root:
                if not sub.tag.endswith('port'):
                    continue
                self.portName = sub.attrib['name']
                for addr in sub:
                    url = addr.attrib['location']
                    self.location = "/".join(url.split('/')[3:])
    
    def ports(self):
        """获取port"""
        for sub in self.documents:
            try:
                if sub.tag.endswith('portType'):
                    if sub.attrib['name'] == self.portName:
                        soap_port = sub
            except Exception as e:
                print(f'{e}')
        if soap_port:
            for oper in soap_port:
                yield oper.attrib['name']

    def gen_config(self):
        """生成配置"""
        self.bindings()
        config = {
            self.location:{

            }
        }
        for port in self.ports():
            config[access_point][port] = "{}.xml".format(port)
        return config
