"""Elastic DB Storage class

Author: Sudipto Nandi

Copyrights: MentorLink 2020-2021

Description: This class implements the Storage Abstract class for
elasticdb
"""
from datetime import datetime
import hashlib
from common_modules.util.singleton import singleton
from common_modules.storage.storage_base import StorageBase
from elasticsearch import Elasticsearch, exceptions
from common_modules.logger.mnt_logging import MntLogging as MyLog
import common_modules.config.elastic_config as elastic_config


def str_to_id(text):
    if text.isdigit():
        return int(text)
    m = hashlib.md5()
    m.update(text.encode())
    id_val = str(int(m.hexdigest(), 16))[0:13]
    return id_val


def get_idsearch_query(id: list):
    search_param = {
        "query": {
            "ids": {
                "values": id
            }
        }
    }
    return search_param


def get_keysearch_query(filter_param):
    filters = []
    for key, value in filter_param.items():
        filters.append({'match': {key: value}})
    search_param = {'query': {'bool': {'must': filters}}}
    return search_param


@singleton
class StorageElastic(StorageBase):
    """
    This class is actual implementation of the abstract class
    for ElasticDb.
    """

    MAX_SEARCH_SIZE = 1000

    def __init__(self,
                 logger=MyLog().setloglevel('debug'),
                 ip=elastic_config.remote_host,
                 port=elastic_config.remote_port,
                 dbname=elastic_config.cluster_name,
                 cleanup=True):
        """
        Constructor of StorageElastic Class.

        :param ip: The IP address of DB
        :type ip: str
        :param port: The Port on which ElasticDb is opened.
        :type port: str
        :param dbname: Database Name
        :type dbname: str
        """
        self._logger = logger
        self.cleanup = cleanup
        super().__init__(dbname, cleanup)
        self._logger.debug(
            "Initializing Elastic DB ip:%s port:%s Cluster Name:%s" % (ip, port, dbname))
        self._db = Elasticsearch([ip], cluster_name=dbname,
                                 http_auth=(elastic_config.username,
                                            elastic_config.password),
                                 port=int(port))

    """
    Override create with different signature.
    """

    def create(self, index, body):
        self.CHECK(index, exist=False)
        self._indexes[index] = self._db.indices.create(index=index, body=body, ignore=400)

    def index_exist(self, index):
        return True if self._db.indices.exists(index=index) else False

    def delete(self, index, force=False):
        # self.CHECK(index)
        self._logger.debug("Delete all for collection %s" % index)
        try:
            if force is False:
                del self._indexes[index]
                self._db.indices.delete(index=index)
            else:
                self._db.indices.delete(index=index)

        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("Delete failed for index:%s" % index)
            raise

    def add(self, index, key, value):
        self.CHECK(index)
        self._logger.debug("Collection name: %s Add Key: %s Value %s" % (index, key, value))

        for v in value:
            try:
                if key is not None:
                    id_num = str_to_id(key)
                    res = self.search(index=index, body=get_idsearch_query([str(id_num)]), raw=True)
                else:
                    res = None
                    id_num = None
                if (res is not None) and (len(res) != 0):
                    self._logger.debug(f"Returned result {res}")
                    res = res[0]
                    if 'id' in res.keys():
                        del res['id']
                    res = v
                    res['updated'] = datetime.now()
                    res = self._db.index(index=index, id=id_num, body=res)
                    self._db.indices.refresh(index=index)
                else:
                    v['created'] = datetime.now()
                    v['updated'] = datetime.now()
                    res = self._db.index(index=index, id=id_num, body=v)
                    self._db.indices.refresh(index=index)
            except Exception as ex:
                self._logger.info(ex)
                self._logger.critical("create failed for index:%s key:%s post:%s" % (index, key, v))
                raise
            else:
                self._logger.debug(
                    "Inserted entries for Key: %s is %s in Collection %s" % (key, res, index))

    def remove(self, index, key):
        self.CHECK(index)
        self._logger.debug("Delete Key: %s" % key)
        try:
            id_num = str_to_id(key)
            res = self._db.delete(index=index, id=id_num)
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("delete failed for index:%s key:%s" % (index, key))
            raise
        self._logger.debug("Delete Key: %s is successful" % key)

    def read(self, index, key):
        """if index not in self._indexes.keys():
            raise Exception("Sorry, the collection does not exist")"""
        try:
            if len(key) != 0:
                id_num = str_to_id(key)
                res = self._db.get(index=index, id=id_num)
            else:
                return self.search(index)
        except exceptions.NotFoundError:
            self._logger.debug("Entry not found key: %s" % key)
            return []
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("find failed for index:%s key:%s" % (index, key))
            raise
        self._logger.debug("Read Collection: %s Key: %s val: %s" % (index, key, res))

        return [res['_source']]

    def update(self, index, key, data):
        self._logger.debug("Collection name: %s Add Key: %s Value %s" % (index, key, data))
        print("Collection name: %s Add Key: %s" % (index, key))
        id_num = str_to_id(key)
        try:
            res = self.search(index, get_idsearch_query([str(id_num)]))
            if res:
                old_data = res[0]

                # remove any id that may be stored in the old data
                if 'id' in old_data:
                    del old_data['id']

                # Make sure old data stays and add / update any new data
                for key, value in data.items():
                    old_data[key] = value
                    data = old_data
                self._logger.debug("Collection name: %s Updating Key: %s" % (index, key))
        except:
            data['created'] = datetime.now()
            pass

        self._logger.debug("Collection name: %s Creating Key: %s" % (index, key))
        print("Collection name: %s Creating Key: %s" % (index, key))
        data['updated'] = datetime.now()

        res = self._db.index(index=index, id=id_num, body=data)
        self._db.indices.refresh(index=index)
        self._logger.debug(
            "Inserted/Updated entries for Key: %s is %s in Collection %s" % (key, res, index))

    def search_raw(self, index, body):
        """
        Return raw response from elastic search results.
        """
        rec = []
        res = self._db.search(index=index, body=body, scroll='2m', size=self.MAX_SEARCH_SIZE, request_timeout=60)
        scroll_id = res['_scroll_id']
        page = res['hits']['hits']
        rec += page
        while len(page):
            res = self._db.scroll(scroll_id=scroll_id, scroll='2m')
            scroll_id = res['_scroll_id']
            page = res['hits']['hits']
            rec += page

        self._logger.debug(f"Result is  {rec}")
        return rec

    def search(self, index, body=None, raw=False):
        """
        Clean raw responses and store them in a list.
        """
        body_search = {}
        if raw is True:
            body_search = body
        elif body is None:
            body_search = {'query': {'match_all': {}}}
        else:
            body_search = get_keysearch_query(body)
        self._logger.debug(f"Search with {body_search}")
        try:
            res = self.search_raw(index=index, body=body_search)
            count = len(res)
            self._logger.debug(f"Got {count} Hits:")
            results = list()
            for hit in res:
                hit["_source"]["id"] = hit["_id"]
                self._logger.debug(f'{hit["_source"]}')
                results.append(hit["_source"])
            return results
        except exceptions.NotFoundError:
            self._logger.debug("Entry not found key: %s" % body)
            return []
        except Exception as ex:
            self._logger.info(ex)
            self._logger.critical("find failed for index:%s key:%s" % (index, body))
            raise

    def search_with_filters(self, index, filter_param):
        filters = list()
        for key, value in filter_param.items():
            filters.append({'match': {key: value}})
        body = {'query': {'bool': {'must': filters}}}
        return self.search(index, body, raw=True)

    def aggregate_counter(self, index: str, base_field: str, aggr_fields: dict = None):
        """
        Collect aggregated results from elastic search.
        :param index: Table/Collection name.
        :param base_field: Field name to group stats.
        :param aggr_fields: Key is field name for stats aggregating.
                            Value is filter criteria. if Value is
                            'None' means create array and store all
                            values into this array. Caller will decide what it wants
                            to do with this array.
                            If aggr_fields is not provided, simply count base_field.
        :return: A counter of dict type.
                Keys are unique values searched from index based on base_field.
                Values are aggregated stats of aggr_fields or counts of base_field.
        """

        def read_entry(e, field):
            """
            Helper to read entry value from nested dictionary.
            :param e: Entry, row of the data.
            :param field: Nested column name joined by '.'.
            :return: Value.
            """
            # TODO: optimize split
            fields = field.split('.')
            for f in fields:
                # TODO: fix this, could be multi-dict entries in a list
                # Should multi-activities be stored in separate entry???
                if isinstance(e, list):
                    e = e[0]
                e = e[f]
            return e

        select_fields = [base_field]
        if aggr_fields:
            select_fields += aggr_fields.keys()
        # Query to collect selected info
        entries = self.search(index, body={
            '_source': select_fields,
            'query': {'match_all': {}}
        }, raw=True)
        counters = dict()
        for entry in entries:
            # Find base keys for counters.
            # If it's only single key, convert it to a list for code unification.
            base_keys = read_entry(entry, base_field)
            if not isinstance(base_keys, list):
                base_keys = [base_keys]
            for base_key in base_keys:
                # Initialize if it's a new base field
                if base_key not in counters:
                    if aggr_fields:
                        counters[base_key] = dict()

                        # Some uses cases require to get the value for given entry
                        # Some uses cases require to count how many times it occurred.
                        # To accommodate both uses case, caller when setting aggr_value= = None
                        #   means that caller wants all the values to be copied as arrays and
                        #   send it back to caller, for all other cases use existing count based
                        #   tracking
                        for aggr_key, aggr_value in aggr_fields.items():
                            if aggr_value is None:
                                # Caller wants to copy all values in array
                                counters[base_key][aggr_key] = []
                            else:
                                # Caller wants to track how may times it occured
                                counters[base_key][aggr_key] = 0
                    else:
                        counters[base_key] = 0

                # If there are aggregate fields, only increment matching counter.
                # Otherwise, simply increment counter on base key.
                if aggr_fields:
                    for aggr_key, aggr_value in aggr_fields.items():
                        entry_value = read_entry(entry, aggr_key)
                        # if caller gave value as None then expected output
                        # need to add entry_value into array
                        if aggr_value is None:
                            if isinstance(entry_value, list):
                                counters[base_key][aggr_key].extend(entry_value)
                            else:
                                counters[base_key][aggr_key].append(entry_value)
                        elif entry_value == aggr_value or not aggr_value:
                            counters[base_key][aggr_key] += 1
                else:
                    counters[base_key] += 1
        return counters

    def get_storage_type(self):
        return "ElasticDb"

    def updateset(self, index, key, subkey, value):
        pass

    def updateunset(self, index, key, subkey, field):
        pass
