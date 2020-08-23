#!/usr/bin/python
#coding=utf8
import click
import json
from wsdl import WSDLService, wsdl_from_url
from server import start_server

EMPTY_SOAP_RESPONSE = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
  </soap12:Body>
</soap12:Envelope>
"""


@click.group()
def cli():
    pass


@click.command()
@click.argument('wsdl')
def project(wsdl):
    """
    # 通过WSDL生成对应的配置
    """
    wsdl = wsdl_from_url(wsdl)
    service = WSDLService(wsdl)
    config = service.gen_config()
    with open('./config.json', 'w') as f:
        f.write(json.dumps(config))
    with open('./wsdl.xml') as f:
        f.write(wsdl)
    for port in service.ports():
        with open(f'./{port}.xml', 'w') as f:
            f.write(EMPTY_SOAP_RESPONSE)


@click.command()
@click.argument('port', default="8080")
def serv(port):
    """
    # 启动Mock Server
    """
    with open('./config.json', 'r') as f:
        config = json.loads(f.read())
        start_server(port, config)


def main():
    cli.add_command(project)
    cli.add_command(serv)
    cli()

if __name__ == '__main__':
    main()
