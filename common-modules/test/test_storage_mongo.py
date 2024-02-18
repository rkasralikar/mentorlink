from common_modules.storage.storage_mongo import StorageMongo


class TestClass:
    def setup_method(self):
        self._index = 'unittest'
        self._db = StorageMongo(dbname='TestDb')
        self._db.create(self._index)

    def teardown_method(self):
        self._db.delete(self._index)

    def test_basic(self):
        assert self._db.get_storage_name() == "TestDb"
        assert self._db.get_storage_type() == 'MongoDb'

    def test_create_read(self):
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
        key = "nlp"
        self._db.add(self._index, key, val)
        val = [{
            "name": "basic ML",
            "score": 1,
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
            }]
        key = "ml"
        self._db.add(self._index, key, val)
        read_val = self._db.read(self._index, "ml")
        assert read_val[0]['name'] == "basic ML"
        read_val = self._db.read(self._index, "nlp")
        assert read_val[0]['name'] == "basic nlp"

    def test_delete_read(self):
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
        key = "nlp2del"
        self._db.add(self._index, key, val)
        self._db.remove(self._index, key)
        read_val = self._db.read(self._index, key)
        assert len(read_val) == 0

    def test_update_set_read(self):
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
        self._db.add(self._index, key, val)
        self._db.updateset(self._index, key, {"name": "advanced nlp"}, {"score": 14})
        read_val = self._db.read(self._index, key)
        assert read_val[1]['score'] == 14
        self._db.updateset(self._index, key, {"name": "advanced nlp"}, {"instructor": "Mr. Idiot"})
        read_val = self._db.read(self._index, key)
        assert read_val[1]['instructor'] == "Mr. Idiot"

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
        self._db.add(self._index, key, val)
        self._db.updateset(self._index, key, {"name": "advanced nlp"}, {"instructor": "Mr. Idiot"})
        read_val = self._db.read(self._index, key)
        assert read_val[1]['instructor'] == "Mr. Idiot"
        self._db.updateunset(self._index, key, {"name": "advanced nlp"}, {"instructor": "Mr. Idiot"})
        read_val = self._db.read(self._index, key)
        has_key = 'instructor' in read_val[1].keys()
        assert not has_key
