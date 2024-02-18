import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
import src.datamodel.user_profile_analytics as user_profile_analytics
import json
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic


class TestClass:
    def setup_method(self, method):
        MyLog().setloglevel('debug')
        MyLog().getlogger().info("===== Setup Test Case %s ====" %
                                 method.__name__)

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)

    def test_user_profile_analytics_serialization(self):
        uaobj = user_profile_analytics.UserProfileDataAnalytics(user_id=10000,
                                                                profile_info=
                                                                user_profile_analytics.UserProfileDataAnalyticsInfo(
                                                                    num_saved_feed=10,
                                                                    last_login_time="10:0:0 PST",
                                                                    num_feed_visited=100,
                                                                    total_time_spent=100,
                                                                    search_keywords=["python", "ml"],
                                                                    app_version="0.0.1"
                                                                )
                                                                )
        user_profile_analytics_json_ser = user_profile_analytics.UserProfileDataAnalyticsSchema().dump(uaobj)
        assert len(user_profile_analytics_json_ser) != 0
        assert user_profile_analytics_json_ser['user_id'] == 10000
        assert user_profile_analytics_json_ser['profile_info']['app_version'] == "0.0.1"

    def test_user_profile_data_deserialization(self):
        jos = json.dumps(
            {'profile_info': {'num_feed_visited': 100, 'app_version': '0.0.1', 'total_time_spent': 100,
                              'num_saved_feed': 10, 'search_keywords': ['python', 'ml'],
                              'last_login_time': '10:0:0 PST'}, 'user_id': 10000}
        )
        uobj = user_profile_analytics.UserProfileDataAnalyticsSchema().loads(jos)
        assert len(uobj) != 0
        assert uobj.user_id == 10000
        assert uobj.profile_info.total_time_spent == 100
