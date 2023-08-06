#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Snap Installer
==============
Modified: 2021-02

Handles new snap installations from s3 download location
"""
import os
import shutil
import logging

class Installer:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.tmp = os.environ['SNAP_FP']
        self.name = os.environ['SNAP_NAME']
        self.secrets = os.environ['SNAP_SECRETS']
        self.common = os.environ['SNAP_COMMON']
        self.logger.info("%s instantiated successfully.", __name__)

    def install(self):
        """
        Uninstall existing snap, artificially inject machine secrets from
        secrets to $SNAP_COMMON and install new snap file in devmode.
        """
        self.logger.info("Removing current snap")
        os.system(f"snap stop {self.name}")
        os.system(f"snap remove {self.name}")
        try:
            shutil.copytree(self.secrets, self.common + '/certs')
        except FileNotFoundError as exc:
            self.logger.exception("%s\nIRIS machine secrets not found.\
                Ensure that IMS are present in: ~/.secrets.", exc)
            return
        except FileExistsError:
            self.logger.info(
                "Machine secrets already exist in the correct location.")
        # special hardware dependant files dumped outside certs/
        os.system(
            f'mv {self.common}/certs/hardware.env {self.common}/hardware.env'
        )
        self.logger.debug("hardware.env moved to %s successfully", self.common) 
        os.system(f"snap install {self.tmp} --devmode")
        self.logger.info("snap installed successfully")
