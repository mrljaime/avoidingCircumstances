# coding=utf-8

import os
import ConfigParser
import logging


"""
    Loading configuration 
"""
config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(os.pardir)), "config", "app.ini"))


"""
    Def logging
"""
logger = logging.getLogger("Seproban stuff")
handler = logging.FileHandler(config.get("app", "logCompletePath"))

if "debug" == config.get("app", "logLevel"):
    logger.setLevel(level=logging.DEBUG)
    handler.setLevel(level=logging.DEBUG)
elif "info" == config.get("app", "logLevel"):
    logger.setLevel(level=logging.INFO)
    handler.setLevel(level=logging.INFO)
else:
    print("There's no config for logging")
    exit(1)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)