#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import hashlib
import json
import logging
import os
import time
import uuid

from aos_provisioning.onboard.board_base import BoardBase
from aos_provisioning.utils.connectors import SerialConnector
from aos_provisioning.utils.errors import BoardError

logger = logging.getLogger(__name__)


class Board(BoardBase):
    PATH_SYSTEM_UID = '/var/aos/system_uid.txt'
    PATH_SM_CERTS = '/var/aos'

    OLD_PATH_VIS_CFG = '/var/aos/vis/visconfig.json'
    OLD_PATH_UM_CFG = '/var/aos/updatemanager/aos_updatemanager.cfg'
    OLD_PATH_SERVICE_MANAGER_CFG = '/var/aos/servicemanager/aos_servicemanager.cfg'

    CONFIGS_FOLDER = '/etc/aos/'
    CERTIFICATES_FOLDER = '/var/aos/crts/'

    SERVICE_MANAGER_CONFIG_FILENAME = 'aos_servicemanager.cfg'
    UPDATE_MANAGER_CONFIG_FILENAME = 'aos_updatemanager.cfg'
    VIS_CONFIG_FILENAME_1 = 'visconfig.json'
    VIS_CONFIG_FILENAME_2 = 'aos_vis.cfg'
    MODEL_FILE_NAME = 'model_name.txt'
    HW_ID_FILE_NAME = 'hardware_id.txt'

    def __init__(self, port, cred):
        super(Board, self).__init__()
        self._port = port
        self._cred = cred

    def init_connector(self):
        serial = SerialConnector(self._port, self._cred)
        serial.connect()

        return serial

    def get_init_data(self):
        """ Read aos-updatemanager config on board and find in it places where to store certificates and keys.
            Find aos-servicemanager config and store it location in config.

            Raises:
                BoardError: If config file was not found on the board on known places.
            Returns:
                None
        """

        self.create_dir("/var/aos")
        # Default key names and directories are in old places
        self.config.online_key_folder = Board.PATH_SM_CERTS
        self.config.online_key_filename = 'unit_online.pem.key'
        self.config.online_cert_folder = Board.PATH_SM_CERTS

        self.config.online_cert_filename = 'unit_online.pem.crt'
        self.config.online_csr_filename = 'unit_online.pem.csr'
        self.config.offline_key_folder = Board.PATH_SM_CERTS
        self.config.offline_key_filename = 'unit_offline.pem.key'
        self.config.offline_cert_folder = Board.PATH_SM_CERTS
        self.config.offline_cert_filename = 'unit_offline.pem.crt'
        self.config.offline_csr_filename = 'unit_offline.pem.csr'
        self.config.target_resources_file_path = '/var/aos/resources/available_configuration.cfg'

        self._set_slashes_to_paths_end()

    def get_hw_id(self):
        logger.info("Obtaining hardware ID ...")

        logger.debug("Running AOS provisioning script STEP1")
        while True:
            try:
                ret = self.connector.execute_script("/xt/scripts/aos-provisioning.step1.sh")
                if ret.exit_code:
                    logger.error("Failed to run AOS provisioning script STEP1")
                    raise AssertionError
                break
            except ValueError:
                pass
        logger.debug("AOS provisioning script STEP1 successful finished")

        self._config.hw_id = self.read_file("/var/aos/hardware_id.txt")

    def get_system_id(self):
        logger.info("Obtaining vin ...")
        if not self.is_file_exist(Board.PATH_SYSTEM_UID):
            logger.info("System UID found.... Initializing board ")
            self.connector.execute_script("/xt/scripts/aos-provisioning.step2.sh get_system_uid")
            logger.info("Script aos-provisioning.step2.sh get_system_uid")
        if self.is_file_exist(Board.PATH_SYSTEM_UID):
            self._config._system_id = self.read_file(self.PATH_SYSTEM_UID)
        else:
            logger.error("System UID not defined")
            return None

    def _generate_pair(self, pair_type):
        data = self.read_file("/var/aos/{}.pem.csr".format(pair_type))
        data = data.strip("-----END CERTIFICATE REQUEST-----")
        data = data.strip("-----BEGIN CERTIFICATE REQUEST-----")
        data = data.strip()
        data = "-----BEGIN CERTIFICATE REQUEST-----\n" + data + '\n-----END CERTIFICATE REQUEST-----\n'
        return data

    def configure(self):
        logger.info("Configuring the board ...")
        logger.debug("Putting certificates...")
        logger.debug("Putting info...")
        self.write_to_file("/var/aos/system_uid.txt", self.config.system_id)
        self.write_to_file("/var/aos/claim.txt", self.config.user_claim)
        time.sleep(1)
        self._save_cert_to_file("/var/aos/unit_online.pem.crt", self.config.online_certificate)
        time.sleep(1)
        self._save_cert_to_file("/var/aos/unit_offline.pem.crt", self.config.offline_certificate)
        time.sleep(.5)
        self._set_target_resources()

        logger.debug("Running AOS provisioning script STEP2")
        while True:
            try:
                ret = self.connector.execute_script("/xt/scripts/aos-provisioning.step2.sh")
                if ret.exit_code:
                    logger.error("Failed to run AOS provisioning script STEP2")
                    raise AssertionError
                break
            except ValueError:
                pass
        logger.debug("AOS provisioning script STEP2 successful finished")


    def _save_cert_to_file(self, file_name, file_content):
        logger.info("Upload cert {} to board".format(file_name))
        _CERT_END = "-----END CERTIFICATE-----\n"
        _CERT_END_NOT_NL = "-----END CERTIFICATE-----"

        chunks = file_content.split(_CERT_END)

        while True:
            try:
                self.connector.execute("rm -f {}".format(file_name), debug=False)
            except ValueError:
                pass

            for chunk in chunks:
                if chunk not in [_CERT_END, _CERT_END_NOT_NL, ""]:
                    cmd = "echo '{}' >> {}".format(chunk + _CERT_END_NOT_NL, file_name)
                    self.connector.send(cmd)
            time.sleep(1.5)
            self.connector.send("\x03")
            time.sleep(1)
            self.connector.execute('clear')
            self.connector.clear()

            resp = self.connector.execute("test -e {}".format(file_name))
            if resp.exit_code:
                logger.error("Uploaded file not found. Retrying upload...")
                continue

            if not self._validate_content_upload(file_content, file_name):
                logger.error("Uploaded file checksum is wrong. Retrying upload...")
                continue
            else:
                logger.info("File {} uploaded successfully.".format(file_name))
                break

    def _set_target_resources(self):
        if self.config.target_resources is not None:
            self.config.target_resources = json.dumps(self.config.target_resources, indent=4)
            self.write_to_file('/var/aos/resources_config.cfg', self.config.target_resources)
            cmd_create_dir = "ssh root@192.168.0.3  \"mkdir -p /var/aos/resources \""
            cmd_copy = "RESOURCES_CONFIG = \"$(cat /var/aos/resources_config.cfg)\""
            cmd_paste = "ssh root@192.168.0.3 \"echo ${RESOURCES_CONFIG} > /var/aos/resources/available_configuration.cfg \""
            self.connector.send(cmd_create_dir)
            self.connector.send(cmd_copy)
            self.connector.send(cmd_paste)
        else:
            cmd_touch = "ssh root@192.168.0.3  \"touch /var/aos/resources_config.cfg \""
            self.connector.send(cmd_touch)

    def perform_deprovisioning(self):
        logger.debug("Running AOS deprovisioning script")
        while True:
            try:
                ret = self.connector.execute_script("/xt/scripts/aos-provisioning.step2.sh deprovisioning")
                if ret.exit_code:
                    logger.error("Failed to run AOS deprovisioning script")
                    raise AssertionError
                break
            except ValueError:
                pass
        logger.debug("AOS deprovisioning script successful finished")
        print("Deprovisioning finished successfully")

    def get_model_name(self):
        """ Obtains model name and version"""
        logger.info("Obtaining model name ...")

        if self.is_file_exist(BoardBase.PATH_MODEL_NAME):
            model_name = self.read_file(BoardBase.PATH_MODEL_NAME)
        else:
            model_name = "Dev board; Unknown"

        if isinstance(model_name, bytes):
            model_name = model_name.decode()

        if not model_name:
            logger.info(" .. model name is absent. Please update you VM image with a fresh copy!")
            return "DevKit", "0.1"

        model_name_chunks = model_name.strip().split(";")
        model_name_name_chunk = model_name_chunks[0].strip()
        if len(model_name_chunks) > 1:
            model_name_version_chunk = model_name_chunks[1].strip()
        else:
            model_name_version_chunk = "0.1"

        logger.info(" .. model name: '{}' version: '{}'".format(model_name_name_chunk, model_name_version_chunk))
        self._config.model_name = model_name_name_chunk
        self._config.model_version = model_name_version_chunk
        return model_name_name_chunk, model_name_version_chunk
