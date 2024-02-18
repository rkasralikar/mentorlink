"""Mongo DB Storage class

Author: Sudipto Nandi

Copyrights: MentorLink 2020-2021

Description: This class implements the Storage Abstract class for
Mongodb
"""
from pymongo import MongoClient
from common_modules.util.singleton import singleton
from common_modules.storage.storage_base import StorageBase


@singleton
class StorageMongo(StorageBase):
    """
    This class is actual implementation of the abstract class
    for MongoDB.
    """

    def __init__(self, ip='localhost', port='27017', dbname='Mentorlink'):
        """
        Constructor of StorageMongo Class.

        :param ip: The IP address of DB
        :type ip: str
        :param port: The Port on which MongoDB is opened.
        :type port: str
        :param dbname: Database Name
        :type dbname: str
        """
        super().__init__(dbname)
        self._logger.debug("Initializing Mongo DB ip:%s port:%s Name:%s" % (ip, port, dbname))
        mongo_client = MongoClient(ip, int(port))
        self._db = mongo_client[dbname]

    def create(self, index, body):
        self.CHECK(index, exist=False)
        self._indexes[index] = self._db[index]

    def delete(self, index, force):
        self.CHECK(index)
        self._logger.debug("Delete all for collection %s" % index)
        try:
            self._indexes[index].drop()
            del self._indexes[index]
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("Delete failed for index:%s" % index)
            raise

    def add(self, index, key, value):
        self.CHECK(index)
        self._logger.debug("Collection name: %s Create Key: %s Value %s" % (index, key, value))
        post = []

        for v in value:
            v.update({"mkey": key})
            post.append(v)

        try:
            insertedentries = self._indexes[index].insert_many(post)
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("Create failed for index:%s key:%s post:%s" % (index, key, post))
            raise
        else:
            self._logger.debug(
                "Inserted entries for Key: %s is %s in Collection %s" % (key, insertedentries, index))

    def remove(self, index, key):
        self.CHECK(index)
        self._logger.debug("Delete Key: %s" % (key))
        try:
            self._indexes[index].delete_many({"mkey": key})
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("delete failed for index:%s key:%s" % (index, key))
            raise

    def read(self, index, key):
        self.CHECK(index)
        ret = []
        try:
            retentries = self._indexes[index].find({"mkey": key})
            self._logger.info("Returned values are %s" % retentries)
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("find failed for index:%s key:%s" % (index, key))
            raise
        for ent in retentries:
            del ent['mkey']
            del ent['_id']
            ret.append(ent)
        self._logger.debug("Read Collection: %s Key: %s val: %s" % (index, key, ret))
        return ret

    def updateset(self, index, key, subkey, value):
        self.CHECK(index)
        self._logger.debug("Updateset Collection: %s Key: %s Value %s" % (index, key, value))
        newkey = {}
        newkey.update({"mkey": key})
        newkey.update(subkey)
        try:
            retval = self._indexes[index].update_many(newkey, {"$set": value})
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("update failed for index:%s key:%s" % (index, key))
            raise
        self._logger.debug("Update Collection: %s Key: %s val: %s" % (index, newkey, retval))

    def updateunset(self, index, key, subkey, field):
        self.CHECK(index)
        self._logger.debug("Updateunset Collection: %s Key: %s subkey %s" % (index, key, subkey))
        newkey = {}
        newkey.update({"mkey": key})
        newkey.update(subkey)
        try:
            retval = self._indexes[index].update_many(newkey, {"$unset": field})
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("updateunset failed for index:%s key:%s" % (index, key))
            raise
        self._logger.debug("Update Collection: %s Key: %s val: %s" % (index, key, retval))

    def get_storage_type(self):
        return "MongoDb"

