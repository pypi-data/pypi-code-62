##
# File: serverStatus.py
# Date: 11-Aug-2020
#
##
# pylint: skip-file
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/status", tags=["status"])
def serverStatus():
    return {"msg": "Status is nominal!"}


@router.get("/", tags=["status"])
def rootServerStatus():
    return {"msg": "Service is up!"}


@router.get("/healthcheck", tags=["status"])
def rootHealthCheck():
    return "UP"
