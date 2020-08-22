#!/usr/bin/env python3
import os
import json
import singer
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema
import requests
from odata import ODataService

from discover import discover
from sync import sync

REQUIRED_CONFIG_KEYS = ["start_date", "username", "password", "environment", "tenantId"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def do_discover(service):
    LOGGER.info("Starting discovery")
    catalog = discover(service)
    return catalog

@utils.handle_top_exception(LOGGER)
def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    url = "https://api.businesscentral.dynamics.com/v2.0/{}/{}/api/BCSItera/dashboards/v1.0/".format(args.config["tenantId"], args.config["environment"])
    service = ODataService(
        url,
        reflect_entities=True,
        auth=requests.auth.HTTPBasicAuth(args.config["username"], args.config["password"])
    )
    catalog = args.catalog or do_discover(service)
    
    if args.discover:
        catalog = discover(service)
        catalog.dump()

    else:
        sync(service, catalog, args.state, args.config["start_date"],)

if __name__ == "__main__":
    main()
