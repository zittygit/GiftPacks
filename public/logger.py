#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import re
from logging.handlers import TimedRotatingFileHandler
from pprint import pformat


class Logger:
    def __init__(self, module):
        self.logger = logging.getLogger(module)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s : %(message)s", "%Y-%m-%d %H:%M:%S")
        log_file_handler = TimedRotatingFileHandler(filename="logs/%s.log" % module, when="D", interval=1, backupCount=7)
        log_file_handler.suffix = "%Y%m%d"
        log_file_handler.extMatch = re.compile(r"^\d{4}\d{2}\d{2}$")
        log_file_handler.setFormatter(formatter)
        log_file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(log_file_handler)

    def error(self, message, exc_info=False):
        self.logger.error(message, exc_info=exc_info)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def pretty_error(self, message):
        self.logger.error(pformat(message, width=180))

    def pretty_info(self, message):
        self.logger.info(pformat(message, width=180))

    def pretty_debug(self, message):
        self.logger.debug(pformat(message, width=180))
