import pytest
from common_modules.storage.storage_mongo import StorageMongo
from common_modules.storage.resource_mgr import ResourceMgr
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
        self._resource_mgr = ResourceMgr(StorageMongo(dbname='UnitTestDb'))

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)
        del self._resource_mgr

    def test_basic(self):
        assert self._resource_mgr._db.get_storage_name() == "UnitTestDb"
        assert self._resource_mgr._db.get_storage_type() == 'MongoDb'

    def test_resource_mgr_create_read(self):
        val = [{
            "name": "basic ML",
            "score": 10,
            "provider": "coursera",
            "url": "https://www.coursera.org/browse/data-science/machine-learning",
            "online": True,
            "paid": False
        },
            {
                "name": "advanced ML",
                "score": 2,
                "provider": "coursera",
                "url": "https://www.coursera.org/browse/data-science/machine-learning",
                "online": True,
                "paid": False
            },
            {
                "name": "advanced ML",
                "score": 9,
                "provider": "coursera",
                "url": "https://www.coursera.org/browse/data-science/machine-learning",
                "online": True,
                "paid": False
            }]
        key = "ml"
        self._resource_mgr.add("test_index_name", key, val, resource_data_index_mapping)
        read_val = self._resource_mgr.read("test_index_name", "ml")
        assert read_val[0]["score"] == 10
        assert read_val[1]["score"] == 9
        assert read_val[2]["score"] == 2

    def test_resource_mgr_create_delete_read(self):
        val = [{
            "name": "basic ML",
            "score": 10,
            "provider": "coursera",
            "url": "https://www.coursera.org/browse/data-science/machine-learning",
            "online": True,
            "paid": False
        },
            {
                "name": "advanced ML",
                "score": 2,
                "provider": "coursera",
                "url": "https://www.coursera.org/browse/data-science/machine-learning",
                "online": True,
                "paid": False
            },
            {
                "name": "advanced ML",
                "score": 9,
                "provider": "coursera",
                "url": "https://www.coursera.org/browse/data-science/machine-learning",
                "online": True,
                "paid": False
            }]
        key = "ml"
        self._resource_mgr.add("test_index_name", key, val)
        self._resource_mgr.remove("test_index_name", key)
        read_val = self._resource_mgr.read("test_index_name", key)
        assert len(read_val) == 0

    def test_update_set_read(self):
        val = [{
            "name": "basic nlp",
            "score": 13,
            "provider": "coursera",
            "url": "https://www.coursera.org/lecture/neural-networks-deep-learning/welcome-Cuf2f",
            "online": True,
            "paid": True
        },
            {
                "name": "advanced nlp",
                "score": 10,
                "provider": "coursera",
                "url": "https://www.coursera.org/lecture/neural-networks-deep-learning/welcome-Cuf2f",
                "online": True,
                "paid": True
            }]
        key = "nlp4update"
        self._resource_mgr.add("test_index_name", key, val)
        read_val = self._resource_mgr.read("test_index_name", key)
        assert read_val[0]['name'] == "basic nlp"
        self._resource_mgr.updateset("test_index_name", key, {"name": "advanced nlp"}, {"score": 14})
        read_val = self._resource_mgr.read("test_index_name", key)
        assert read_val[0]['name'] == "advanced nlp"

    def test_update_unset_read(self):
        val = [{
            "name": "basic nlp",
            "score": 10,
            "provider": "coursera",
            "url": "https://www.coursera.org/lecture/neural-networks-deep-learning/welcome-Cuf2f",
            "online": True,
            "paid": True
        },
            {
                "name": "advanced nlp",
                "score": 11,
                "provider": "coursera",
                "url": "https://www.coursera.org/lecture/neural-networks-deep-learning/welcome-Cuf2f",
                "online": True,
                "paid": True
            }]
        key = "nlp4update"
        self._resource_mgr.add("test_index_name", key, val)
        self._resource_mgr.updateset("test_index_name", key, {"name": "advanced nlp"}, {"instructor": "Mr. Idiot"})
        read_val = self._resource_mgr.read("test_index_name", key)
        assert read_val[0]['instructor'] == "Mr. Idiot"
        self._resource_mgr.updateunset("test_index_name", key, {"name": "advanced nlp"}, {"instructor": "Mr. Idiot"})
        read_val = self._resource_mgr.read("test_index_name", key)
        has_key = 'instructor' in read_val[0].keys()
        assert not has_key
