"""  Items class for StackOverflow
Author: Amit Grover

Copyrights: MentorLink 2021-2022

Description: This class implements
the Items Abstract class.
"""

from src.businesslogic.items import Items
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_local import StorageLocal
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.util.tags_normalization import transform_tags as tran_tags
from enum import Enum, IntEnum


class ScoreRange(IntEnum):
    Score_Data_Min = 0,
    Score_Data_Max = 100,
    Score_Max = 5


#
# We should figure out if we can scrape number of
# comments and score based on that rather than attendees.
# Score Range is  0 - > 5
def get_score(attendees):
    score = (attendees // (int(ScoreRange.Score_Data_Max) - int(ScoreRange.Score_Data_Min))) * int(ScoreRange.Score_Max)
    return score


class ItemsMeetup(Items):
    def __init__(self,
                 table_name=None):
        self.table_name = table_name
        self.provider = "meetup"

    def get_data(self, resource_mgr=ResourceMgr(StorageLocal())):
        data = resource_mgr.read(self.table_name, '')
        for d in data:
            MyLog().getlogger().debug(f"Data from meetup {d}")
            ret_data = {"name": d['title'], "url": d['url'], "description": d['title'],
                        "provider": self.provider, "online": True, "paid": False,
                        "score": get_score(int((d['attendees'].split())[0])),
                        "tags": list({tran_tags(t) for t in d['tags']}), "native_item_identifier": str(d['id']),
                        "native_table_name": self.table_name}
            yield ret_data
