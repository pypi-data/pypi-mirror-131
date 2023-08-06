#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/17 15:29
# @Author  : Adyan
# @File    : logger.py



import logging
import os
import datetime


class LoggerClass:
    level_relations = {"debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING,
                       "error": logging.ERROR, "critical": logging.CRITICAL, }
    fmt_str = "%(asctime)s - %(levelname)s : %(message)s"
    logFile = 'log'

    def __init__(self, level='info', fmt=fmt_str):
        if not os.path.exists(self.logFile):
            os.makedirs(self.logFile)
        formatter = logging.Formatter(fmt)
        filename = self.logFile + '/' + datetime.datetime.today().strftime('%Y-%m-%d') + '.txt'

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.level_relations.get(level))

        self.filelogger = logging.FileHandler(filename, encoding='utf-8')
        self.filelogger.setFormatter(formatter)

    def info(self, message, level="info"):

        self.logger.addHandler(self.filelogger)
        if level == "debug" or level == "DEBUG":
            self.logger.debug(message)
        elif level == "info" or level == "INFO":
            self.logger.info(message)
        elif level == "warning" or level == "WARNING":
            self.logger.warning(message)
        elif level == "error" or level == "ERROR":
            self.logger.error(message)
        elif level == "critical" or level == "CRITICAL":
            self.logger.critical(message)
        else:
            raise ("日志级别错误")
        self.logger.removeHandler(self.filelogger)
