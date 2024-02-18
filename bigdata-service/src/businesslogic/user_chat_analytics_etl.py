import pdb

import requests
import json
import threading
import datetime
from src.businesslogic.etl_jobs import EtlJobs
from src.datamodel.user_chat_analytics import UserChatAnalytics, UserChatAnalyticsSchema
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_local import StorageLocal
from common_modules.logger.mnt_logging import MntLogging as MyLog

user_chat_analytics_mapping = {
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
            "chat_info": {
                "properties": {
                    "peer_list": {
                        "type": "integer"
                    },
                    "group_list": {
                        "type": "integer"
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


class EtlJObUserChatAnalytics(EtlJobs):
    def __init__(self, end_point: str, user_name: str, password: str, login_url: str,
                 resource_mgr=ResourceMgr(StorageLocal()), table_name="user_chat_analytics_etl_0",
                 mapping_name=None):
        if mapping_name is None:
            mapping_name = user_chat_analytics_mapping
        self.end_point = end_point
        self.user_name = user_name
        self.password = password
        self.login_url = login_url
        self.resmgr = resource_mgr
        self.table_name = table_name
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
            MyLog().getlogger().info(ex)
            MyLog().getlogger().debug("Login failed for user chat analytcs etl")
            return False

    def start(self):
        page = 1
        while True:
            data = {'pageNo': page, 'recordsPerPage': 100}
            try:
                response = requests.post(url=self.end_point,
                                     data=json.dumps(data), headers=self.headers)
                if response.status_code != 200:
                    break
            except Exception as ex:
                MyLog().getlogger().info(ex)
                MyLog().getlogger().debug("API call failed for user chat analytics etl")
                break
            data_resp = response.json()
            if len(data_resp['data']) == 0:
                break
            for item in data_resp['data']:
                try:
                    uobj = UserChatAnalyticsSchema().loads(json.dumps(item))
                    MyLog().getlogger().debug(f'Success {uobj}')
                    #key = str(item['user_id'])
                    key = None
                    self.resmgr.add(self.table_name, key, UserChatAnalyticsSchema().dump(uobj), self.mapping_name)
                except Exception as ex:
                    MyLog().getlogger().info(ex)
                    MyLog().getlogger().debug(f"Invalid data obtained {item}")

            page += 1
