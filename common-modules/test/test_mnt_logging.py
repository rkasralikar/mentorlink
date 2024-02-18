import logging
from common_modules.logger.mnt_logging import MntLogging
import os
import re

class TestClass:
    def setup_method(self):
        """
        Log path is fixed once MntLogging singleton is created.
        """
        self._log_path = ('D:\\tmp\\' if os.name == 'nt' else '/tmp/') + 'test_log_file.txt'
        self._logger = MntLogging(filename=self._log_path)

    def test_log_singleton(self):
        assert self._logger.getlogfilepath() == self._log_path
        assert self._logger == MntLogging()
        assert self._logger.getlogger() == MntLogging().getlogger()
        assert self._logger.getlogger().getEffectiveLevel() == logging.ERROR

    def test_log_level(self):
        self._logger.setloglevel('debug')
        assert self._logger.getlogger().getEffectiveLevel() == logging.DEBUG
        self._logger.setloglevel('error')
        assert self._logger.getlogger().getEffectiveLevel() == logging.ERROR

    def test_log_debug_messages(self):
        start_lines = self._read_lines()
        self._logger.setloglevel('debug')
        self._logger.getlogger().info("Hello World")
        self._logger.setloglevel('error')
        end_lines = self._read_lines()
        assert len(end_lines) == len(start_lines) + 1
        assert re.match('.*INFO.*Hello World.*', end_lines[-1])

    def test_log_critical_messages(self):
        """
        INFO message is not logged.
        """
        start_lines = self._read_lines();
        self._logger.setloglevel('critical')
        self._logger.getlogger().info("Hello World")
        end_lines = self._read_lines();
        assert len(end_lines) == len(start_lines)

        """
        CRITICAL message is logged.
        """
        start_lines = self._read_lines()
        self._logger.getlogger().critical("Hello World2")
        end_lines = self._read_lines()
        assert len(end_lines) == len(start_lines) + 1
        assert re.match('.*CRITICAL.*Hello World2.*', end_lines[-1])

    def _read_lines(self):
        file = open(self._log_path, 'r')
        lines = file.readlines()
        file.close()
        return lines
