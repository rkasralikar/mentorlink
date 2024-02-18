"""  User activity ETL
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema class for item info query response class.
"""
import pdb
import time
import requests
import json
import threading
import datetime
from src.businesslogic.etl_jobs import EtlJobs
from src.businesslogic.items import Items
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_local import StorageLocal
from common_modules.logger.mnt_logging import MntLogging as MyLog

normalized_item_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "name": {
                "type": "text"
            },
            "url": {
                "type": "text"
            },
            "description": {
                "type": "text"
            },
            "provider": {
                "type": "text"
            },
            "online": {
                "type": "boolean"
            },
            "paid": {
                "type": "boolean"
            },
            "score": {
                "type": "double"
            },
            "upvotecount": {
                "type": "integer"
            },
            "downvotecount": {
                "type": "integer"
            },
            "sharecount": {
                "type": "integer"
            },
            "tags": {
                "type": "text"
            },
            "native_item_identifier": {
                "type": "text"
            },
            "native_table_name": {
                "type": "text"
            },
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            }
        }
    }
}


class EtlJObItemNormalization(EtlJobs):
    def __init__(self, end_point: str, user_name: str, password: str, login_url: str,
                 item_src: list[Items],
                 resource_mgr=None,
                 table_name=None,
                 mapping_name=None):
        if mapping_name is None:
            mapping_name = normalized_item_mapping
        if table_name is None:
            table_name = "item_normalization_table_etl_new"
        self.end_point = None
        self.user_name = None
        self.password = None
        self.login_url = None
        self.item_src = item_src
        if resource_mgr is None:
            self.resmgr = ResourceMgr(StorageLocal())
        else:
            self.resmgr = resource_mgr
        self.table_name = table_name
        self.mapping_name = mapping_name
        self.headers = None

    def login(self):
        return True

    def start(self):
        data = {}
        for items in self.item_src:
            for data in items.get_data(self.resmgr):
                while True:
                    try:
                        item_info = self.resmgr.search(self.table_name, {"url": data['url']})
                        break
                    except Exception as ex:
                        MyLog().getlogger().error(f"Exception occured {ex}")
                        time.sleep(300)
                if len(item_info) != 0:
                    data['upvotecount'] = item_info[0]['upvotecount']
                    data['downvotecount'] = item_info[0]['downvotecount']
                    data['sharecount'] = item_info[0]['sharecount']
                else:
                    data['upvotecount'] = 0
                    data['downvotecount'] = 0
                    data['sharecount'] = 0
                MyLog().getlogger().debug(f"Data obtained {data}")
                key = (data['native_item_identifier'])+"-"+data['url']
                # pdb.set_trace()
                while True:
                    try:
                        self.resmgr.add(self.table_name, key, data, self.mapping_name)
                        break
                    except Exception as ex:
                        MyLog().getlogger().error(f"Exception occured {ex}")
                        time.sleep(300)
