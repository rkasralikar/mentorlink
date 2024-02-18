"""Abstract StorageBase class

Author: Sudipto Nandi

Copyrights: MentorLink 2020-2021

Description: This is the definition of Abstract class
for all the storage types used by recommender service.
"""

from common_modules.logger.mnt_logging import MntLogging as MyLog

class StorageBase:
    _db = None
    _dbname = None
    _indexes = None
    _logger = None

    def __init__(self, dbname, cleanup=True):
        """
        Constructor for basic db info. Can be overwritten.
        """
        MyLog().setloglevel('debug')
        self._dbname = dbname
        self.cleanup = cleanup
        self._indexes = {}
        self._logger = MyLog().getlogger()

    def __del__(self):
        """
        Destructor for basic db info. Can be overwritten.
        """
        if self.cleanup:
            for index in self._indexes:
                index.drop()

    def __call__(self, *args, **kwargs):
        """
        Callable method.
        """
        pass

    def create(self, index, body):
        """
        Creating collection in the database

        :param index: Collection name
        :type index: str
        :param body: Collection Mapping
        :type body: dict
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def delete(self, index, force=False):
        """
        Delete Collection in the database, it drops all the documents
        of that collection.

        :param index: Collection name
        :type index: str
        :param force: if true then it will delete the index forcefully
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def add(self, index, key, value):
        """
        Api to add an entry to the collection.

        :param index: Collection name
        :type index: str
        :param key: Key to the entry, a unique identifier
        :type key: dict
        :param value: The dictionary to be added.
        :type value: dict
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def remove(self, index, key):
        """
        API to remove an entry from the collection.
        :param index: Collection name
        :type index: str
        :param key: Key to the document, a unique identifier
        :type key: dict:
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def read(self, index, key):
        """
        Read API for the database entry

        :param index: Collection name
        :type index: str
        :param key: Key to the entry, a unique identifier
        :type key: dict
        :return: Returns the value at the key
        :rtype: dict
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def search(self, index: str, body: dict):
        """

        :param index: Collection name
        :param body: Search query. Currently only supported for Elastic.
        :return: Returns entries collected from response.
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def updateset(self, index, key, subkey, value):
        """
        Update set is the APi which modifies an existing entry.
        In case if the entry doesnt exist, it will add the entry.

        :param index: Collection name
        :type index: str
        :param key: Key to the document, a unique identifier
        :type key: dict
        :param subkey: The subkey to identify the element to update in the doc.
        :type subkey: dict
        :param value: The value to set
        :type value: dict
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def updateunset(self, index, key, subkey, field):
        """
        Update unset is the API to delete a partial fields of an entry.

        :param index: Collection name
        :type index: str
        :param key: Key to the document, a unique identifier
        :type key: dict:
        :param subkey: The subkey to identify the element to update in the doc.
        :type subkey: dict
        :param value: The value to set
        :type value: dict
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def get_storage_type(self):
        """
        Get the storage type of the instantiated database.

        :return: The type of instantiated database. Example Mongo, elastic
        :rtype: str
        """
        raise NotImplementedError(f"Abstract method in {__name__}.")

    def get_storage_name(self):
        """
        Name of the DB instance.

        :return: Name of the database.
        :rtype: str
        """
        return self._dbname

    def CHECK(self, index, exist=True):
        if (index in self._indexes) is not exist:
            exist = index in self._indexes
            message = f"Sorry, the collection {index} " + ("already exists." if exist else "does not exist.")
            self._logger.debug(message)
            raise Exception(message)
