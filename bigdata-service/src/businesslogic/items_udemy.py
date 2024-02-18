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
import numpy as np


def convert_float(x):
    try:
        return round(float(x), 2)
    except:
        return 0.0


def sigmoid(x):
    try:
        x = round(float(x), 2)
    except:
        return 0.0
    c1 = 0.09
    c2 = 25
    return round(1 - (1 / (1 + np.exp(c1 * (x - c2)))), 2)
    # MYTODO: Sometimes getting a warning "RuntimeWarning: overflow encountered in exp"


def get_score(ratings: float, num_rev: int):
    score = ratings * sigmoid(convert_float(num_rev))
    return round(score, 2)


class ItemsUdemy(Items):
    def __init__(self,
                 table_name=None):
        self.table_name = table_name
        self.provider = "udemy"

    def get_data(self, resource_mgr=ResourceMgr(StorageLocal())):
        data = resource_mgr.read(self.table_name, '')
        for d in data:
            MyLog().getlogger().debug(f"Data from Udemy {d}")
            float_lam = lambda x: 0.0 if x is None else float(x)
            int_lam = lambda x: 0 if x is None else int(x)
            ret_data = {"name": d['title'], "url": d['url'], "description": d['desc'],
                        "provider": self.provider, "online": True, "paid": True,
                        "score": get_score(float_lam(d['ratings']), int_lam(d['num_reviews'])),
                        "tags": [tran_tags(t) for t in d['tags']], "native_item_identifier": str(d['id']),
                        "native_table_name": self.table_name}
            yield ret_data
