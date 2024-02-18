import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
import json
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
from src.businesslogic.item_normalization_etl import EtlJObItemNormalization
from src.businesslogic.items_udemy import ItemsUdemy


class TestClass:
    def setup_method(self, method):
        MyLog().setloglevel('debug')
        MyLog().getlogger().info("===== Setup Test Case %s ====" %
                                 method.__name__)

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)

    def test_item_normalization(self):
        etl_norm = EtlJObItemNormalization(end_point="", user_name="", password="", login_url="",
                                           item_src=[ItemsUdemy(table_name="resource_data_documents_rev1")],
                                           resource_mgr=ResourceMgr(StorageElastic()))
        etl_norm.start()
