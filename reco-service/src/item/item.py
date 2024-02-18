"""  Item class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements the Abstract class for Items
"""
from common_modules.logger.mnt_logging import MntLogging as MyLog
from heapq import heapify, heappop, heappush
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic


class Item:
    def __init__(self, table_name='item_normalization_table_etl_new', score_pred=None, tags_list=None, top_n=100):
        """
        Constructor for the item class. This class will be used to read
        the resources for the given tags_list and find the top_n
        items based on the score_predicate.

        :param table_name: Table name from where to pull the data
        :param score_predicate: A predicate to generate score from the data.
        :param tags_list : List of tags
        :param top_n: Top N items in every tags
        """
        if tags_list is None:
            tags_list = ['python', 'machinelearning', 'java']
        self.table_name = table_name
        self.item_dict = {}
        self.tags_list = tags_list
        self.top_n = top_n
        MyLog().getlogger().info(
            f"Instantiation of item class for table name {self.table_name} tags-list {self.tags_list}")

    def __call__(self, *args, **kwargs):
        pass

    def process(self, resmgr=None):
        """
        The method to process the resource data from DB, clean the data and generate the score for
        the resource
        """
        if resmgr is None:
            resmgr = ResourceMgr(StorageElastic())
        MyLog().getlogger().info("Process is called for resource from %s" % self.table_name)
        for tag in self.tags_list:
            search_param = {"tags": tag}
            retry_count = 5
            while retry_count:
                try:
                    data = resmgr.search(self.table_name, search_param=search_param)
                    break
                except Exception as ex:
                    MyLog().getlogger().info(ex)
                    MyLog().getlogger().debug(f"Retry again retry_count:{retry_count}")
                    retry_count = -1
                    if retry_count == 0:
                        raise
                    continue

            if len(data) == 0:
                continue
            MyLog().getlogger().info(f"Fetched data is {len(data)}")
            heap_data = []
            max_entries = min(self.top_n, len(data))
            for row in data:
                heappush(heap_data, (-1.0 * row['score'], row['id']))
            self.item_dict.update({tag: [heappop(heap_data)[1] for i in range(max_entries)]})

    def table_name(self):
        """
        Return the name of the table for this item
        """
        return self.table_name

    def get_item_dict(self):
        return self.item_dict

    def __del__(self):
        """
        Cleanup the data if stored any.
        """
        MyLog().getlogger().info("Delete is called for item class ")
