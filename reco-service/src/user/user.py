"""  User class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements the User class.
"""
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
from src.item.item import Item
from pdb import set_trace as st
from common_modules.util.tags_normalization import transform_tags as tran_tags


def get_popular_interest():
    return {"python", "java", "machinelearning", "aws", "javascript"}


class User:
    def __init__(self, user_id: int, user_profile_table='user_profile_data_etl_0',
                 resmgr=ResourceMgr(StorageElastic()), max_reco=500, interest_list=None):
        '''
        The constructor will
        :param user_id:
        '''
        tags_list_ent = set()
        self.user_id = user_id
        self.user_profile_table = user_profile_table
        self.resmgr = resmgr
        self.recommendation = set()
        self.max_reco = max_reco
        if interest_list is None or len(interest_list) == 0:
            interest_list = None
        user_data = self.resmgr.read(index=self.user_profile_table, key=str(self.user_id))
        saved_feed = []
        if interest_list is not None:
            tags_list_ent = {tran_tags(interest) for interest in interest_list if len(interest) != 0}
        if len(user_data) != 0:
            user_data[0]['profile_data']['saved_items'] = []
            saved_feed = user_data[0]['profile_data']['saved_items']
            MyLog().getlogger().debug(f"User-id {self.user_id} has interest list {user_data[0]['profile_data']['interest']}")
            for tag in user_data[0]['profile_data']['interest']:
                if len(tag) != 0:
                    tags_list_ent.add(tag)
            if len(tags_list_ent) == 0:
                MyLog().getlogger().debug(f"No interest list found, falling back to popular choice")
                tags_list_ent = get_popular_interest()
            MyLog().getlogger().debug(f"Final Tags list for user-id {self.user_id} is {tags_list_ent}")
        elif interest_list is None:
            MyLog().getlogger().debug(f"No indication given for the user {self.user_id}"
                                      " about interest, falling back to popular choice")
            tags_list_ent = get_popular_interest()

        count_zero = 5
        while (count_zero != 0):
            item = Item(tags_list=list(tags_list_ent), top_n=self.max_reco)
            item.process(resmgr=self.resmgr)
            rec_dict = item.get_item_dict()
            MyLog().getlogger().debug(f"Empty recommendation dict for tag list {tags_list_ent}")
            if len(rec_dict) != 0:
                break
            tags_list_ent = get_popular_interest()
            count_zero-=1

        MyLog().getlogger().debug(f"Final item dict is {rec_dict}")
        items_list = []
        for key, value in rec_dict.items():
            items_list.append(value[:self.max_reco])
        zip_list = list(zip(*items_list))
        tmp_list = []
        for zitem in zip_list:
            for itm in zitem:
                tmp_list.append(itm)
        zip_list = tmp_list
        MyLog().getlogger().debug(f"zip list item is {zip_list}")
        zip_set = set(zip_list)
        for l in items_list:
            for i in l:
                if i not in zip_set:
                    zip_list.append(i)
        MyLog().getlogger().debug(f"Final zip list item is {zip_list}")
        reco_iter = iter(zip_list)
        len_zip_list = len(zip_list)
        MyLog().getlogger().debug(f"len_zip_list: {len_zip_list} and max_reco is {self.max_reco}")
        max_loop_size = min(len_zip_list, self.max_reco)
        i = 0
        while i < len_zip_list:
            recommendation = zip_list[i]
            if recommendation not in saved_feed:
                self.recommendation.add(recommendation)
                if len(self.recommendation) >= max_reco:
                    break
            i+=1

    def get_recommendation(self):
        MyLog().getlogger().debug(f"Returned recommendaton for user_id {self.user_id} are {self.recommendation}")
        return list(self.recommendation)
