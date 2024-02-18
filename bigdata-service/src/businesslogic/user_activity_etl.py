"""  User activity ETL
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema class for item info query response class.
"""
import pdb

import requests
import json
import threading
import datetime
from src.businesslogic.etl_jobs import EtlJobs
from src.datamodel.user_activity import UsersInfoSchema, UserActivitySchema
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_local import StorageLocal
from common_modules.logger.mnt_logging import MntLogging as MyLog
from src.businesslogic.item_normalization_etl import normalized_item_mapping

user_activity_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "user_id": {
                "type": "long"
            },
            "activity": {
                "properties": {
                    "item_id": {
                        "type": "long"
                    },
                    "activity_info": {
                        "properties": {
                            "shared": {
                                "type": "boolean"
                            },
                            "liked": {
                                "type": "boolean"
                            },
                            "disliked": {
                                "type": "boolean"
                            },
                            "saved": {
                                "type": "boolean"
                            },
                            "visit": {
                                "type": "boolean"
                            }
                        }
                    }
                }
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


class EtlJObUserActivity(EtlJobs):
    def __init__(self, end_point: str, user_name: str, password: str, login_url: str,
                 resource_mgr=ResourceMgr(StorageLocal()), table_name=None,
                 mapping_name=None, item_table=None):
        if mapping_name is None:
            mapping_name = user_activity_mapping
        if table_name is None:
            table_name = "user_activity_data_etl_0"
        self.end_point = end_point
        self.user_name = user_name
        self.password = password
        self.login_url = login_url
        self.resmgr = resource_mgr
        self.table_name = table_name
        if item_table is None:
            item_table = "item_normalization_table_etl"
        self.item_table = item_table
        self.mapping_name = mapping_name
        self.headers = {'content-type': 'application/json', 'accept': 'application/json'}

    def login(self):
        data = {'email': self.user_name, 'password': self.password}
        try:
            response = requests.post(url=self.login_url,
                                     data=json.dumps(data), headers=self.headers)
            self.headers['x-access-token'] = response.json()['data']['token']
            return True
        except Exception as ex:
            MyLog().getlogger().error(ex)
            MyLog().getlogger().error("Login failed for user activity etl")
            return False

    def start(self):
        page = 1
        count = 1
        while True:
            data = {'pageNo': page, 'recordsPerPage': 100}
            try:
                response = requests.post(url=self.end_point,
                                     data=json.dumps(data), headers=self.headers)
                if response.status_code != 200:
                    break
            except Exception as ex:
                MyLog().getlogger().error(ex)
                MyLog().getlogger().error("API call failed for user activity etl")
                break
            data_resp = response.json()
            if len(data_resp['data']) == 0:
                break
            for item in data_resp['data']:
                try:
                    del item['_id']
                    del item['createdAt']
                    del item['updatedAt']
                    del item['__v']
                    for act in item['activity']:
                        del act['_id']
                    uobj = UserActivitySchema().loads(json.dumps(item))
                    MyLog().getlogger().debug(f'Success {uobj}')
                    # key = str(item['user_id'])
                    key = None
                    self.resmgr.add(self.table_name, key, UserActivitySchema().dump(uobj), self.mapping_name)
                    # Update the item normalization table as well.
                    for activity_id in uobj.activity:
                        MyLog().getlogger().debug(f"User {uobj.user_id} has item_id {activity_id.item_id} with "
                                                  f"activity info {activity_id.activity_info}")
                        item_data = self.resmgr.read(self.item_table, str(activity_id.item_id))
                        if len(item_data) != 0:
                            MyLog().getlogger().debug(f"Item  {item_data[0]}")
                            data_mod = False
                            if activity_id.activity_info.liked is True:
                                data_mod = True
                                item_data[0]['upvotecount'] += 1
                            if activity_id.activity_info.disliked is True:
                                data_mod = True
                                item_data[0]['downvotecount'] += 1
                            if activity_id.activity_info.shared is True:
                                data_mod = True
                                item_data[0]['sharecount'] += 1
                            if data_mod is True:
                                self.resmgr.add(self.item_table, "7296070827837", item_data, normalized_item_mapping)

                except Exception as ex:
                    MyLog().getlogger().error(ex)
                    MyLog().getlogger().error(f"Invalid data obtained {item}")

            page += 1
