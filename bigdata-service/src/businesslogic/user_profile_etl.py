import pdb

import requests
import json
import threading
import datetime
import re
from src.businesslogic.etl_jobs import EtlJobs
from src.datamodel.user_profile import UserProfileData, UserProfileDataSchema
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_local import StorageLocal
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.util.tags_normalization import transform_tags as tran_tags

keyword_table_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    }
}

user_profile_mapping = {
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
            "profile_data": {
                "properties": {
                    "name": {
                        "type": "text"
                    },
                    "email": {
                        "type": "text"
                    },
                    "phone": {
                        "type": "text"
                    },
                    "about": {
                        "type": "text"
                    },
                    "total_exp": {
                        "type": "integer"
                    },
                    "linkedin_profile": {
                        "type": "text"
                    },
                    "sign_in_method": {
                        "type": "text"
                    },
                    "interest": {
                        "type": "text"
                    },
                    "experience": {
                        "properties": {
                            "company_name": {
                                "type": "text"
                            },
                            "role_desc": {
                                "type": "text"
                            },
                            "start_date": {
                                "type": "text"
                            },
                            "end_date": {
                                "type": "text"
                            }
                        }
                    },
                    "skills": {
                        "type": "text"
                    },
                    "saved_items": {
                        "type": "long"
                    }
                }
            },
            "device_data": {
                "properties": {
                    "device_id": {
                        "type": "text"
                    },
                    "manufacturer": {
                        "type": "text"
                    },
                    "os_ver": {
                        "type": "text"
                    },
                    "app_ver": {
                        "type": "text"
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


class EtlJObUserProfile(EtlJobs):
    def __init__(self, end_point: str, user_name: str, password: str, login_url: str,
                 resource_mgr=ResourceMgr(StorageLocal()), table_name="user_profile_data_etl_0",
                 mapping_name=None, interest_list_sink="resource_table_keyword"):
        if mapping_name is None:
            mapping_name = user_profile_mapping
        self.end_point = end_point
        self.user_name = user_name
        self.password = password
        self.login_url = login_url
        self.resmgr = resource_mgr
        self.table_name = table_name
        self.mapping_name = mapping_name
        self.interest_list = set()
        self.headers = {'content-type': 'application/json', 'accept': 'application/json'}
        self.interest_list_sink = interest_list_sink

    def login(self):
        data = {'email': self.user_name, 'password': self.password}
        try:
            response = requests.post(url=self.login_url,
                                     data=json.dumps(data), headers=self.headers)
            self.headers['x-access-token'] = response.json()['data']['token']
            return True
        except Exception as ex:
            MyLog().getlogger().error(ex)
            MyLog().getlogger().error("Login failed for user profile etl")
            return False

    def start(self):
        page = 1
        MyLog().getlogger().debug("Starting user profile etl")
        while True:
            data = {'pageNo': page, 'recordsPerPage': 100}
            try:
                response = requests.post(url=self.end_point,
                                         data=json.dumps(data), headers=self.headers)
                if response.status_code != 200:
                    break
            except Exception as ex:
                MyLog().getlogger().error(ex)
                MyLog().getlogger().error("API call failed for user profile etl")
                break
            data_resp = response.json()
            if len(data_resp['data']) == 0:
                MyLog().getlogger().error("No Data received in etl call")
                break
            for item in data_resp['data']:
                try:
                    del item['_id']
                    uobj = UserProfileDataSchema().loads(json.dumps(item))
                    MyLog().getlogger().debug(f'Success {uobj}')
                    key = str(item['user_id'])
                    uobj.profile_data.interest = [tran_tags(tag) for tag in uobj.profile_data.interest]
                    for interest in uobj.profile_data.interest:
                        if not bool(re.search(r'\d', interest)):
                            self.interest_list.add(interest)
                    self.resmgr.add(self.table_name, key, UserProfileDataSchema().dump(uobj), self.mapping_name)
                except Exception as ex:
                    MyLog().getlogger().error(ex)
                    MyLog().getlogger().error(f"Invalid data obtained {item}")

            page += 1
        for interest in self.interest_list:
            try:
                self.resmgr.add(self.interest_list_sink, interest, {"keyword": interest}, keyword_table_mapping)
            except Exception as ex:
                MyLog().getlogger().error(ex)
