import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
import src.datamodel.user_chat_analytics as user_chat_analytics
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

    def test_user_chat_analytics_serialization(self):
        uaobj = user_chat_analytics.UserChatAnalytics(user_id=10000,
                                                      chat_info=
                                                      user_chat_analytics.UserChatAnalyticsInfo(
                                                          peer_list=[10001, 10002],
                                                          group_list=[20001, 20002])
                                                      )
        user_chat_analytics_json_ser = user_chat_analytics.UserChatAnalyticsSchema().dump(uaobj)
        assert len(user_chat_analytics_json_ser) != 0
        assert user_chat_analytics_json_ser['user_id'] == 10000
        assert user_chat_analytics_json_ser['chat_info']['peer_list'][0] == 10001

    def test_user_profile_data_deserialization(self):
        jos1 = json.dumps(
            {'chat_info': {'group_list': [20001, 20002], 'peer_list': [10001, 10002]}, 'user_id': 10000}
        )
        jos2 = json.dumps({'user_id': 1, 'chat_info': {'peer_list': [9, 10], 'group_list': [10]}})
        uobj = user_chat_analytics.UserChatAnalyticsSchema().loads(jos1)
        assert len(uobj) != 0
        assert uobj.user_id == 10000
        assert uobj.chat_info.group_list[0] == 20001
        uobj = user_chat_analytics.UserChatAnalyticsSchema().loads(jos2)
        assert len(uobj) != 0
        assert uobj.user_id == 1
        assert uobj.chat_info.group_list[0] == 10
