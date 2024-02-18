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


class ItemsRssFeed(Items):
    def __init__(self,
                 table_name=None):
        self.table_name = table_name
        self.provider = "rssfeed"

    def get_data(self, resource_mgr=ResourceMgr(StorageLocal())):
        data = resource_mgr.read(self.table_name, '')
        for d in data:
            MyLog().getlogger().debug(f"Data from Rss Feed {d}")
            ret_data = {"name": d['title'], "url": d['url'], "description": d['title'],
                        "provider": self.provider, "online": True, "paid": False,
                        "score": d['score'],
                        "tags": list({tran_tags(t) for t in d['tags']}), "native_item_identifier": str(d['id']),
                        "native_table_name": self.table_name}
            yield ret_data
