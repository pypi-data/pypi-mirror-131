# -*- coding: utf-8 -*-
"""
IRIS Staging Client
===================
Modified: 2021-12
"""

__all__ = ['__version__']

import logging
import logging.config
from iris_stage.__version__ import __version__

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)
logging.info("Incuvers™ iris-stage version: %s", __version__)
