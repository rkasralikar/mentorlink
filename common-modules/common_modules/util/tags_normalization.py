"""  Items class for Udemy
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Items Abstract class.
"""

from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
import re
from pdb import set_trace as st

tag_normalizer_set = [
    {frozenset({"amazonwebservicesaws",
                "amazonwebservices",
                "aws"}): "aws"},
    {frozenset({"machinelearning",
                "pytorch",
                "r",
                "tensorflow",
                "neuralnetworks",
                "ai",
                "sklearn",
                "scikitlearn"}): "machinelearning"}
]


def transform_tags(tag: str):
    pattern = "[\s+.\\-_/\\\]+"
    tag = tag.lower()
    tag = re.sub(pattern, '', tag)
    for ts in tag_normalizer_set:
        for k in ts.keys():
            if tag in k:
                tag = ts[k]
                break
    return tag


class ItemsNormalizer:
    def __init__(self,
                 table_name=None):
        if table_name is None:
            table_name = ['resource_data_documents_rev1']
        self.tables_name = table_name
        self.tags_set = set()

    def get_data(self, resource_mgr=ResourceMgr(StorageElastic())):
        tags_set = set()
        for table_name in self.tables_name:
            data = resource_mgr.read(table_name, '')
            for d in data:
                for tag in d['tags']:
                    tags_set.add(tag)
        for tag in tags_set:
            print(transform_tags(tag))
            self.tags_set.add(transform_tags(tag))

    def get_tag_set(self):
        return self.tags_set


def main():
    item = ItemsNormalizer()
    item.get_data()


if __name__ == "__main__":
    main()
