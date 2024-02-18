import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
from src.recomgr.reco_mgr import RecommendationMgr, start_recommendation_generation
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
import json


class TestClass:
    def setup_method(self, method):
        self.reco_mgr = RecommendationMgr(resmgr = ResourceMgr(StorageElastic()))
        MyLog().setloglevel('info')
        MyLog().getlogger().info("===== Setup Test Case %s ====" %
                                 method.__name__)

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)

    def test_user_list_method(self):
        ids = self.reco_mgr.get_user_id_list()
        MyLog().getlogger().info(ids)
        assert len(ids) != 0

    def test_recomgr_method(self):
        reco = self.reco_mgr.generate_recommendation_for_users()
        for key, value in reco.items():
            MyLog().getlogger().error(f"User:{key} Recommendation:{value}")
        assert len(reco) != 0

    def test_periodic_recomgr_gen_method(self):
        start_recommendation_generation(sleep_val=30*60).join()