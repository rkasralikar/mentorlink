"""  Recommendation Manager class
Author: Sudipto Nandi

Copyrights: MentorLink 2022-2023

Description: This class implements the class which will generate.
"""
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
from src.user.user import User
from common_modules.util.singleton import singleton
from pdb import set_trace as st
import threading
import time


@singleton
class RecommendationMgr:
    def __init__(self, user_profile_table_name="user_profile_data_etl_0",
                 resmgr=ResourceMgr(StorageElastic())):
        self.user_profile_table_name = user_profile_table_name
        self.resmgr = resmgr
        self.reco_dict = {}
        self.lock = threading.Lock()

    def get_user_id_list(self):
        user_data = self.resmgr.read(index=self.user_profile_table_name, key="")
        user_id_list = []
        for user_d in user_data:
            user_id_list.append(user_d['user_id'])
        return user_id_list

    def generate_recommendation_for_users(self):
        user_ids = self.get_user_id_list()
        reco_dict = {}
        for user_id in user_ids:
            reco_dict[str(user_id)] = User(user_id=user_id, user_profile_table=self.user_profile_table_name,
                                           resmgr=self.resmgr).get_recommendation()
        reco_dict["default"] = User(user_id=0, user_profile_table=self.user_profile_table_name,
                                    resmgr=self.resmgr).get_recommendation()
        with self.lock:
            self.reco_dict = reco_dict
        return self.reco_dict

    def get_recommendation_for_user(self, user_id="default"):
        with self.lock:
            if user_id in self.reco_dict.keys():
                MyLog().getlogger().debug(f"User-id: {user_id} found in reco_dict")
                recommendation = self.reco_dict[user_id]
            else:
                MyLog().getlogger().info(f"User-id: {user_id} not found in reco_dict")
                recommendation = self.reco_dict["default"]
        MyLog().getlogger().debug(f"Recommendation for User-id: {user_id} is {recommendation}")
        return recommendation


def reco_gen_routiene(user_profile_table_name, resmgr, sleep_val):
    while True:
        MyLog().getlogger().debug(f"Starting the process for recommendation generation for all users")
        RecommendationMgr(user_profile_table_name=user_profile_table_name,
                          resmgr=resmgr).generate_recommendation_for_users()
        MyLog().getlogger().debug(f"Sleeping for {sleep_val}secs, will resume again")
        time.sleep(sleep_val)


def start_recommendation_generation(user_profile_table_name="user_profile_data_etl_0",
                                    resmgr=ResourceMgr(StorageElastic()),
                                    sleep_val=4 * 60 * 60):
    MyLog().getlogger().debug("Starting the thread for recommendation generation")
    thr = threading.Thread(target=reco_gen_routiene, args=(user_profile_table_name, resmgr, sleep_val,))
    thr.start()
    return thr
