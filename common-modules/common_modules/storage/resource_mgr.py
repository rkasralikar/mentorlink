"""Mongo DB Storage class

Author: Sudipto Nandi

Copyrights: MentorLink 2020-2021

Description: This class implements the resource manager. This layer is the
glue between the rest interface and the storage.
"""
from common_modules.logger.mnt_logging import MntLogging as MyLog


class ResourceMgr:
    """
    Resource Manager class is responsible for the main business logic.
    Resource manager is the added layer, which manages the storage class.
    """

    def __init__(self, db, cleanup=True):
        """
        Constructor for resource manager. It will be managing the storage object.
        We are using composition design pattern to avoid any circular dependencies.

        :param db: Storage class object, the object to be managed.
        :type db: storage
        """
        self._db = db
        self.cleanup = cleanup
        self._number_of_entries_per_index = {}
        MyLog().getlogger().info("Instantiating %s database of type %s" %
                                 (self._db.get_storage_name(),
                                  self._db.get_storage_type()))

    def __del__(self):
        """
        Destructor for the resource manager class. This will initiate any cleanup
        or the held resources.
        """
        if self.cleanup:
            # Cannot call MyLog here as its destructor is already called and has released all resource
            # MyLog().getlogger().info("Destructor is called %s" % self._number_of_entries_per_index)
            for index in self._number_of_entries_per_index:
                # Cannot call MyLog here as its destructor is already called and has released all resource
                # MyLog().getlogger().info("Cleaning %s database of type %s"
                #                          " collection %s" %
                #                          (self._db.get_storage_name(),
                #                           self._db.get_storage_type(), index))
                self._db.delete(index)

    def __call__(self, *args, **kwargs):
        pass

    def create(self, index, body):
        return self._db.create(index, body)

    def index_exist(self, index):
        return self._db.index_exist(index)

    def add(self, index, key, data, body={}):
        """
        This will create an entry in the underlying storage.
        It will also do some book keeping so that we can release all
        the resources we allocated.

        :param index: Collection Name
        :type index: str
        :param key: Unique identifier to the entry.
        :type key: str
        :param data: Data to be added.
        :type data: dict
        :param body: Mapping of the entry
        :type body: dict
        """
        datac = []
        if len(data) == 0:
            MyLog().getlogger().info("data is empty")
            return
        elif type(data) is list:
            datac = data
        else:
            datac.append(data)
        if index not in self._number_of_entries_per_index:
            MyLog().getlogger().info("Create collection is called for DB %s:%s" %
                                     (self._db.get_storage_name(),
                                      index))
            self._db.create(index, body)
            self._number_of_entries_per_index[index] = 0
        self._number_of_entries_per_index[index] += 1
        MyLog().getlogger().info("Create entry is called for DB %s:%s "
                                 "key: %s value:%s" %
                                 (self._db.get_storage_name(),
                                  index, key, datac))
        return self._db.add(index, key, datac)

    def delete(self, index, force=False):
        if index not in self._number_of_entries_per_index:
            if force is False:
                MyLog().getlogger().debug(f"Index {index} do not exists")
                return
        MyLog().getlogger().info("Delete index is called for DB %s:%s "
                                 % (self._db.get_storage_name(), index))
        self._db.delete(index=index, force=force)
        return

    def remove(self, index, key):
        """
        Deletes the entries at the key.

        :param index: Collection Name
        :type index: str
        :param key: Unique identifier
        :type key: str
        """
        MyLog().getlogger().info("Delete entry is called for DB %s:%s "
                                 "key: %s" %
                                 (self._db.get_storage_name(),
                                  index, key))
        if index not in self._number_of_entries_per_index:
            return
        self._number_of_entries_per_index[index] -= 1
        self._db.remove(index, key)
        if self._number_of_entries_per_index[index] == 0:
            MyLog().getlogger().info("Delete index is called for DB %s:%s "
                                     % (self._db.get_storage_name(), index))
            self._db.delete(index)
            del self._number_of_entries_per_index[index]

    def read(self, index, key):
        """
        API to read the entry for a unique identifier and for the specified
        collection name. This API will return the entries reversed sorted by score.

        :param index: Collection Name
        :type index: str
        :param key: Unique identifier to the entry to be read.
        :type key: str
        :raises except: If the DB throws an error. This will not pass the interrupt above.
        :return: Returns the content
        :rtype: dict
        """
        MyLog().getlogger().info("Read entry is called for DB %s:%s "
                                 "key: %s" %
                                 (self._db.get_storage_name(),
                                  index, key))
        try:
            retval = self._db.read(index, key)
        except:
            MyLog().getlogger().critical("DB %s:%s seems to be empty" %
                                         (self._db.get_storage_name(), index))
            retval = {}

        return retval

    def updateset(self, _index, key, subkey, data):
        MyLog().getlogger().info("Read entry is called for DB %s:%s "
                                 "key: %s subkey: %s"
                                 "data: %s" %
                                 (self._db.get_storage_name(),
                                  _index, key, subkey,
                                  data))
        return self._db.updateset(_index, key, subkey, data)

    def updateunset(self, _index, key, subkey, field):
        MyLog().getlogger().info("Read entry is called for DB %s:%s "
                                 "key: %s subkey: %s" %
                                 (self._db.get_storage_name(),
                                  _index, key, subkey))
        return self._db.updateunset(_index, key, subkey, field)

    def search(self, index, search_param=None, raw=False):
        """
        API to search for given search_param and return all entries found or None

        :param raw:
        :param index: Collection Name
        :type index: str
        :param search_param: search param syntax
        :type key: str
        :raises except: If the DB throws an error. This will not pass the interrupt above.
        :return: Returns the content
        :rtype: dict
        """
        MyLog().getlogger().info("Search called for DB %s:%s "
                                 "search_param: %s" %
                                 (self._db.get_storage_name(),
                                  index, search_param))
        return self._db.search(index, search_param, raw)

    def update(self, index, key, data):
        """
        API to update the given key, and if it doesnot exist, creates one.
        This API is little different that add function above. to avoid changing behavior or
        add function adding this update function instead

        :param index: Collection Name
        :type index: str
        :param search_param: search param syntax
        :type key: str
        :param value: value for given key
        :type key: str
        :raises except: If the DB throws an error. This will not pass the interrupt above.
        :return: Returns the content
        :rtype: dict
        """
        MyLog().getlogger().info("Update called for DB %s:%s "
                                 "key: %s value: %s" %
                                 (self._db.get_storage_name(),
                                  index, key, data))
        return self._db.update(index, key, data)

    def aggregate_counter(self, index: str, base_field: str, aggr_fields: dict = None):
        MyLog().getlogger().info("Index %s base_field %s aggr_fields %s" %
                                 (index, base_field, aggr_fields))
        return self._db.aggregate_counter(index, base_field, aggr_fields)
