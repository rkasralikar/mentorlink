"""  Items class for Udemy
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Items Abstract class.
"""

from src.businesslogic.items import Items
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_local import StorageLocal
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.util.tags_normalization import transform_tags as tran_tags


def get_score(view_count, like_count, dislike_count):
    youtube_bias = 4.8
    return youtube_bias + 1.0 * (like_count - dislike_count) / view_count


class ItemsYoutube(Items):
    def __init__(self,
                 table_name=None):
        self.table_name = table_name
        self.provider = "youtube"

    def get_data(self, resource_mgr=ResourceMgr(StorageLocal())):
        data = resource_mgr.read(self.table_name, '')
        for d in data:
            MyLog().getlogger().debug(f"Data from youtube {d}")
            ret_data = {"name": d['title'], "url": d['url'], "description": d['description'],
                        "provider": self.provider, "online": True, "paid": False,
                        "score": get_score(d['view_count'], d['like_count'], d['dislike_count']),
                        "tags": list({tran_tags(t) for t in d['tags']}), "native_item_identifier": str(d['id']),
                        "native_table_name": self.table_name}
            yield ret_data
