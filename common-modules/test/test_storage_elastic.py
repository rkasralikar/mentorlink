from common_modules.storage.storage_elastic import StorageElastic
from common_modules.logger.mnt_logging import MntLogging as MyLog

resource_data_index_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "title": {
                "type": "text"
            },
            "url": {
                "type": "text"
            },
            "desc": {
                "type": "text"
            },
            "inst_list": {
                "type": "text"
            },
            "ratings": {
                "type": "double"
            },
            "num_reviews": {
                "type": "long"
            },
            "tot_time": {
                "type": "double"
            },
            "num_lecs": {
                "type": "text"
            },
            "level": {
                "type": "text"
            },
            "tags": {
                "type": "text"
            },
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            }
        }
    }
}


class TestClass:
    def setup_method(self, method):
        MyLog().setloglevel('debug')
        MyLog().getlogger().info("===== Setup Test Case %s ====" %
                                 method.__name__)
        self._index = 'self._index'
        self._db = StorageElastic()
        self._db.create(index=self._index, body=resource_data_index_mapping)

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)
        self._db.delete(self._index)

    def test_basic(self):
        assert self._db.get_storage_name() == "mentorlink-dl-staging"
        assert self._db.get_storage_type() == 'ElasticDb'

    def test_create_read(self):
        val = [{
            "title": "basic nlp",
            "ratings": 10,
            "num_reviews": 5467,
            "url": "https://www.coursera.org/lecture/neural-networks-deep-learning/welcome-Cuf2f",
            "inst_list": ['A', 'B'],
            "desc": "abcdefgg",
            "tot_time": 1234,
            "num_lecs": "1234",
            "level": "Beginner",
            "tags": ["python", "c++"]
            }]
        key1 = val[0]['url']
        self._db.add(self._index, key1, val)
        val = [{
                "title": "basic ML",
                "ratings": 11,
                "num_reviews": 5467,
                "url": "https://www.coursera.org/learn/machine-learning",
                "inst_list": ['A', 'B'],
                "desc": "abcdefgg",
                "tot_time": 1234,
                "num_lecs": "1234",
                "level": "Beginner",
                "tags": ["python", "c++"]
            }]
        key2 = val[0]["url"]
        self._db.add(self._index, key2, val)
        read_val = self._db.read(self._index, key2)
        assert read_val[0]['title'] == "basic ML"
        read_val = self._db.read(self._index, key1)
        assert read_val[0]['title'] == "basic nlp"

    def test_delete_read(self):
        val = [{
                    "title": "basic ML",
                    "ratings": 11,
                    "num_reviews": 5467,
                    "url": "https://www.coursera.org/learn/machine-learning",
                    "inst_list": ['A', 'B'],
                    "desc": "abcdefgg",
                    "tot_time": 1234,
                    "num_lecs": "1234",
                    "level": "Beginner",
                    "tags": ["python", "c++"]
                }]
        key = val[0]["url"]
        self._db.add(self._index, key, val)
        self._db.remove(self._index, key)
        read_val = self._db.read(self._index, key)
        assert len(read_val) == 0
