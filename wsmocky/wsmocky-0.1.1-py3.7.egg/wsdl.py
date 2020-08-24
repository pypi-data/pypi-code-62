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

    def bindings(self):
        """
        获取入口
        """
        for sub in self.documents:
            print(f'{sub.tag}')
            if sub.tag.endswith('service'):
                service_root = sub
                break
        if service_root:
            for sub in service_root:
                if not sub.tag.endswith('port'):
                    continue
                if sub.attrib['name'].endswith('Soap'):
                    for addr in sub:
                        url = addr.attrib['location']
                        return "/".join(url.split('/')[3:])
    
    def ports(self):
        """获取port"""
        for sub in self.documents:
            if sub.tag.endswith('portType'):
                if sub.attrib['name'].endswith('Soap'):
                    soap_port = sub
        if soap_port:
            for oper in soap_port:
                yield oper.attrib['name']

    def gen_config(self):
        """生成配置"""
        access_point = self.bindings()
        config = {
            access_point:{

            }
        }
        for port in self.ports():
            config[access_point][port] = "{}.xml".format(port)
        return config
