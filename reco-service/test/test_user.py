import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
from recommendation.src.user.user import User
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
import json


class TestClass:
    def setup_method(self, method):
        MyLog().setloglevel('debug')
        MyLog().getlogger().info("===== Setup Test Case %s ====" %
                                 method.__name__)

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)

    def test_user_object(self):
        resmgr = ResourceMgr(StorageElastic())
        user = User(user_id=1016, resmgr=resmgr)
        assert len(user.get_recommendation()) == 100

    def test_unknown_user_object(self):
        resmgr = ResourceMgr(StorageElastic())
        user = User(user_id=587, resmgr=resmgr, interest_list=[''])
        assert len(user.get_recommendation()) == 100
