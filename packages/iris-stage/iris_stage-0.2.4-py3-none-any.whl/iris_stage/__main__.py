# -*- coding: utf-8 -*-
import os
import sys
import yaml
import logging
import logging.config
from pathlib import Path
from iris_stage.srv.srv import StageClient

CONFIG_PATH = Path(__file__).parent.joinpath('logs/config.yaml')

# bind logging to config file
# verify path existance before initializing logger file configuration
try:
    # load config from .yaml
    with open(CONFIG_PATH) as conf:
        logging.config.dictConfig(yaml.load(conf, Loader=yaml.FullLoader))
except FileNotFoundError:
    print("Logging config file not found in expected absolute path: {}"
        .format(CONFIG_PATH))
except Exception as exc:
    print("Logging configuration failed: {}".format(exc))
else:
    print("Logging configuration successful.")


logger = logging.getLogger(__name__)
SERVICE_NAME = os.environ['SERVICE_NAME']
PID_DIR = os.environ['PID_DIR']

if len(sys.argv) != 2:
    sys.exit('Syntax: %s COMMAND' % sys.argv[0])

cmd = sys.argv[1].lower()
# instantiate staging client
service = StageClient(name=SERVICE_NAME, pid_dir=PID_DIR)

if cmd == 'start':
    logger.info("Starting %s service in %s", SERVICE_NAME, PID_DIR)
    service.start()
elif cmd == 'stop':
    logger.info("Halting %s service in %s", SERVICE_NAME, PID_DIR)
    try:
        service.stop()
    except ValueError:
        logger.info("Service %s is not running", SERVICE_NAME)
else:
    sys.exit('Unknown command "%s".' % cmd)
