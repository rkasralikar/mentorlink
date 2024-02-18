"""Local Storage class

Author: Sudipto Nandi

Copyrights: MentorLink 2020-2021

Description: This class implements the Local Storage Abstract class for
Unit Testing
"""
from common_modules.util.singleton import singleton
from common_modules.storage.storage_base import StorageBase
import os
import json
from pdb import set_trace


@singleton
class StorageLocal(StorageBase):
    """
    This class is actual implementation of the abstract class
    for Local Storage which be just the file write.
    """

    def __init__(self, dirname=None, dbname='unit_test'):
        """
        Constructor of Local Storage Class.

        :param dirname: The directory where storage files will be created.
        :type dirname: str
        :param dbname: Database Name
        :type dbname: str
        """
        if dirname:
            self.dirname = dirname
        else:
            self.dirname = "D:\\tmp\\db" if os.name == "nt" else "/tmp/db"
        super().__init__(dbname)
        self._logger.debug("Initializing Local DB dirname:%s DB Name:%s" % (self.dirname, dbname))
        self._indexes = set() # TODO(fcdu) All other storage classes use dictionary
        try:
            os.mkdir(self.dirname)
        except OSError as error:
            self._logger.debug(error)

    def __del__(self):
        """
        Destructor for Storage db.
        """
        for index in self._indexes:
            os.remove(self._path(index))

    def create(self, index, body):
        self.CHECK(index, exist=False)
        self._indexes.add(index)
        f = open(self._path(index), "w")
        f.close()

    def delete(self, index, force):
        self.CHECK(index)
        path = self._path(index)
        self._logger.debug("Delete All for collection %s" % index)
        try:
            os.remove(path)
            self._indexes.remove(index)
        except Exception as ex:
            self._logger.info(ex)

    def add(self, index, key, value):
        self.CHECK(index)
        self._logger.debug("Collection name: %s Create Key: %s Value %s" % (index, key, value))
        path = self._path(index)
        data = {}
        if os.path.getsize(path) != 0:
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecoder as error:
                    self._logger.debug(error)

        data[key] = value
        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    def remove(self, index, key):
        self.CHECK(index)
        self._logger.debug("Delete Key: %s" % key)
        path = self._path(index)
        with open(path, "r") as f:
            data = json.load(f)

        if key in data.keys():
            del data[key]
            self._logger.debug("Delete Key: %s is successful" % key)
            with open(path, 'w') as outfile:
                json.dump(data, outfile)
        else:
            self._logger.debug("Delete Key: %s is Not found" % key)

    def read(self, index, key):
        self.CHECK(index)
        self._logger.debug("Collection name: %s Read Key: %s" % (index, key))
        path = self._path(index)
        with open(path, "r") as f:
            data = json.load(f)

        if len(key) == 0:
            self._logger.debug(data.values())
            ret_buf = []
            for v in data.values():
                ret_buf.append(v[0])

            return ret_buf

        if key in data.keys():
            return data[key]
        # TODO(snandi) other classes are returning empty if read failed
        raise Exception("Sorry, the key does not exist")

    def get_storage_type(self):
        return "LocalDb"

    def _path(self, index):
        return self.dirname + ("\\" if os.name == "nt" else "/") + index

    def updateset(self, index, key, subkey, value):
        pass

    def updateunset(self, index, key, subkey, field):
        pass

