import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
from recommendation.src.item.item import Item
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

    def test_item_object(self):
        resmgr = ResourceMgr(StorageElastic())
        item = Item()
        item.process(resmgr)
        print(f"Python:{item.get_item_dict()['python']}")
        print(f"Java:{item.get_item_dict()['java']}")
