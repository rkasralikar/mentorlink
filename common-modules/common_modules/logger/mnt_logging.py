"""Mentor Link Logging Module

Author: Sudipto Nandi

Copyrights: MentorLink 2020-2021

Description: This module provides logging for all the mentor link modules.
The module is based on python logging infrastructure, it adds
additional functionality like multiple log sink
(console, file or a remote server). Every module can register its own mntlogger.
"""
import datetime
import logging
import os
import sys
from common_modules.util.singleton import singleton


@singleton
class MntLogging:
    """
    MntLogging class implements logging functionality.
    This will be a singleton class, but will act as the mntlogger
    factory for each modules.

    :param _logger: This will hold the python Logger object.
    :type _logger: Logger

    :param _logFilePath: This will hold the log file location.
        Currently we are supporting only one log sink.
    :type _logFilePath: str
    """
    _logger = None
    _logFilePath = None

    def __init__(self, filename=None):
        """
        Initializer of the MntLogging class.

        :param filename: Name of the log sink
        :type filename: str
        """
        self._logger = logging.getLogger("mntlogging")
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        self._logger.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')
        if filename is None:
            now = datetime.datetime.now()
            dirname = "D:\\tmp\\log\\" if os.name == "nt" else "/tmp/log/"
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            # The format of the log would be log_year_month_date.log
            self._logFilePath = dirname + "log_" + now.strftime("%Y-%m-%d_%H%M%S") + ".log"
        else:
            self._logFilePath = filename
        filehandler = logging.FileHandler(self._logFilePath, 'w')
        filehandler.setFormatter(formatter)
        self._logger.addHandler(filehandler)
        self._logger.propagate = False

    def __call__(self, *args, **kwargs):
        pass

    def getlogger(self):
        """
        Will return the mntlogger object for a module

        :return: _logger
        """
        return self._logger

    def getlogfilepath(self):
        """
        Returns the location of the log sink

        :return: _logFilePath
        """
        return self._logFilePath

    def setloglevel(self, level):
        """
        Sets the logging level for a specific module.

        :param level: Level of logging, possible values are
        'debug', 'info', 'warn','error', 'critical'
        :type level: str
        :raises ExceptionType: If the input logging level is
        incorrect
        """
        if level == 'debug':
            self._logger.setLevel(logging.DEBUG)
        elif level == 'info':
            self._logger.setLevel(logging.INFO)
        elif level == 'warn':
            self._logger.setLevel(logging.WARNING)
        elif level == 'error':
            self._logger.setLevel(logging.ERROR)
        elif level == 'critical':
            self._logger.setLevel(logging.CRITICAL)
        else:
            raise Exception('Invalid log level is passed')

