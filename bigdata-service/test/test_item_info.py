import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
import src.datamodel.item_info as item_info
import json
from pdb import set_trace as st


class TestClass:
    def setup_method(self, method):
        MyLog().setloglevel('debug')
        MyLog().getlogger().info("===== Setup Test Case %s ====" %
                                 method.__name__)

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)

    def test_item_info_bulk_serialization(self):
        item_info_bulk_response = [item_info.ItemsInfoResponse(
            item_id=10000,
            item_id_info=item_info.ItemsInfo(name="udemy1",
                                             url="https://www.udemy.com/udemy1",
                                             description="Udemy Course",
                                             provider="Udemy",
                                             online=True,
                                             paid=True,
                                             tags=["machine-learning", "python"],
                                             upvotecount=1,
                                             downvotecount=0,
                                             sharecount=1)
        ), item_info.ItemsInfoResponse(
            item_id=10001,
            item_id_info=item_info.ItemsInfo(name="udemy2",
                                             url="https://www.udemy.com/udemy2",
                                             description="Udemy Course",
                                             provider="Udemy",
                                             online=True,
                                             paid=True,
                                             tags=["machine-learning", "python"],
                                             upvotecount=1,
                                             downvotecount=0,
                                             sharecount=1)
        )]
        uobj = item_info.ItemsInfoBulkResponse(item_list_info=item_info_bulk_response)
        user_item_info_bulk_json_ser = item_info.ItemsInfoBulkResponseSchema().dump(uobj)
        assert user_item_info_bulk_json_ser['item_list_info'][0]['item_id'] == 10000
        assert user_item_info_bulk_json_ser['item_list_info'][1]['item_id'] == 10001

    def test_item_info_bulk_deserialization(self):
        jos = json.dumps(
            {'item_list_info':[{'item_id': 10000, 'item_id_info': {'description': 'Udemy Course 1', 'paid': True, 'online': True,
                                                'provider': 'Udemy', 'name': 'udemy1',
                                                'url': 'https://www.udemy.com/udemy1',
                                                'tags': ['machine-learning', 'python'],
                                                'upvotecount': 1, 'downvotecount': 0, 'sharecount': 1}},
                               {'item_id': 10001,
                                'item_id_info': {'description': 'Udemy Course 2', 'paid': True, 'online': True,
                                                 'provider': 'Udemy', 'name': 'udemy2',
                                                 'url': 'https://www.udemy.com/udemy2',
                                                 'tags': ['machine-learning', 'python'],
                                                 'upvotecount': 1, 'downvotecount': 0, 'sharecount': 1}},
            ]}
        )
        uobj = item_info.ItemsInfoBulkResponseSchema().loads(jos)
        assert len(uobj) != 0
        assert uobj.item_list_info[0].item_id == 10000

    def test_item_info_serialization(self):
        uaobj = item_info.ItemsInfoResponse(item_id=10000,
                                            item_id_info=item_info.ItemsInfo(name="udemy1",
                                                                             url="https://www.udemy.com/udemy1",
                                                                             description="Udemy Course",
                                                                             provider="Udemy",
                                                                             online=True,
                                                                             paid=True,
                                                                             tags=["machine-learning", "python"],
                                                                             upvotecount=1,
                                                                             downvotecount=0,
                                                                             sharecount=1))
        user_item_info_json_ser = item_info.ItemsInfoResponseSchema().dump(uaobj)
        assert len(user_item_info_json_ser) != 0
        assert user_item_info_json_ser['item_id'] == 10000
        assert user_item_info_json_ser['item_id_info']['name'] == "udemy1"

    def test_item_info_deserialization(self):
        jos = json.dumps(
            {'item_id': 10000, 'item_id_info': {'description': 'Udemy Course', 'paid': True, 'online': True,
                                                'provider': 'Udemy', 'name': 'udemy1',
                                                'url': 'https://www.udemy.com/udemy1',
                                                'tags': ['machine-learning', 'python'],
                                                'upvotecount': 1, 'downvotecount': 0, 'sharecount': 1}}
        )
        uobj = item_info.ItemsInfoResponseSchema().loads(jos)
        assert len(uobj) != 0
        assert uobj.item_id == 10000

    def test_item_bulk_info_req_serialization(self):
        uaobj = item_info.ItemInfoBulkRequest(item_id_list=[item_info.ItemInfoRequest(item_id=1001),
                                                            item_info.ItemInfoRequest(item_id=1002)])
        user_item_info_bulk_req_json_ser = item_info.ItemInfoBulkRequestSchema().dump(uaobj)
        assert len(user_item_info_bulk_req_json_ser) != 0

        assert user_item_info_bulk_req_json_ser['item_id_list'][0]['item_id'] == 1001

    def test_item_bulk_info_req_deserialization(self):
        jos = json.dumps(
            {'item_id_list':[{'item_id':1001}, {'item_id':1002}]}
        )
        uobj = item_info.ItemInfoBulkRequestSchema().loads(jos)
        assert len(uobj) != 0
        assert uobj.item_id_list[0].item_id == 1001