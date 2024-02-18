import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
import src.datamodel.user_activity as user_activity
import json


class TestClass:
    def setup_method(self, method):
        MyLog().setloglevel('debug')
        MyLog().getlogger().info("===== Setup Test Case %s ====" %
                                 method.__name__)

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)

    def test_user_activity_serialization(self):
        uaobj = user_activity.UsersInfo(users_info=[
            user_activity.UserActivity(user_id=100, activity=[
                user_activity.Item(item_id=1000,
                                   activity_info=user_activity.ActivityInfo(True, True, True, True, 10, 10, True)),
                user_activity.Item(item_id=1001,
                                   activity_info=user_activity.ActivityInfo(True, True, True, True, 10, 10, True)),
                user_activity.Item(item_id=1002,
                                   activity_info=user_activity.ActivityInfo(True, True, True, True, 10, 10, True))
            ]),
            user_activity.UserActivity(user_id=200, activity=[
                user_activity.Item(item_id=2000,
                                   activity_info=user_activity.ActivityInfo(True, True, True, True, 10, 10, True)),
                user_activity.Item(item_id=2001,
                                   activity_info=user_activity.ActivityInfo(True, True, True, True, 10, 10, True)),
                user_activity.Item(item_id=2002,
                                   activity_info=user_activity.ActivityInfo(True, True, True, True, 10, 10, True))
            ])
        ])
        user_act_json_ser = user_activity.UsersInfoSchema().dump(uaobj)
        assert len(user_act_json_ser) != 0
        assert user_act_json_ser['users_info'][0]['activity'][0]['activity_info']['shared'] == True
        assert user_act_json_ser['users_info'][1]['user_id'] == 200

    def test_user_activity_deserialization(self):
        jos = json.dumps(
            {"users_info": [
                {"user_id": 100, "activity": [
                    {"activity_info": {"rating": 10, "liked": True, "disliked": False, "tot_dur": 10, "shared": True, "saved": True,
                                       "visit": True}, "item_id": 1000},
                    {"activity_info": {"rating": 10, "liked": True, "disliked": False, "tot_dur": 10, "shared": True, "saved": True,
                                       "visit": True}, "item_id": 1001},
                    {"activity_info": {"rating": 10, "liked": True, "disliked": False, "tot_dur": 10, "shared": True, "saved": True,
                                       "visit": True}, "item_id": 1002}]},
                {"user_id": 200, "activity": [
                    {"activity_info": {"rating": 10, "liked": True, "disliked": False, "tot_dur": 10, "shared": True, "saved": True,
                                       "visit": True}, "item_id": 2000},
                    {"activity_info": {"rating": 10, "liked": True, "disliked": False, "tot_dur": 10, "shared": True, "saved": True,
                                       "visit": True}, "item_id": 2001},
                    {"activity_info": {"rating": 10, "liked": True, "disliked": False, "tot_dur": 10, "shared": True, "saved": True,
                                       "visit": True}, "item_id": 2002}]}
            ]}
        )
        print(jos)
        uobj = user_activity.UsersInfoSchema().loads(jos)
        assert len(uobj) != 0
