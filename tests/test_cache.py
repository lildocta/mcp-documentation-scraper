import unittest
from src.cache.local_cache import LocalCache
from src.cache.database import Database

class TestLocalCache(unittest.TestCase):
    def setUp(self):
        self.local_cache = LocalCache()

    def test_cache_document(self):
        doc_id = "test_doc"
        data = {"title": "Test Document", "content": "This is a test."}
        self.local_cache.cache_document(doc_id, data)
        cached_data = self.local_cache.get_document(doc_id)
        self.assertEqual(cached_data, data)

    def test_get_non_existent_document(self):
        doc_id = "non_existent_doc"
        cached_data = self.local_cache.get_document(doc_id)
        self.assertIsNone(cached_data)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database()
        self.database.connect()

    def test_store_and_retrieve_document(self):
        doc_id = "db_test_doc"
        data = {"title": "DB Test Document", "content": "This is a test from DB."}
        self.database.store_document(doc_id, data)
        retrieved_data = self.database.retrieve_document(doc_id)
        self.assertEqual(retrieved_data, data)

    def test_retrieve_non_existent_document(self):
        doc_id = "non_existent_db_doc"
        retrieved_data = self.database.retrieve_document(doc_id)
        self.assertIsNone(retrieved_data)

    def tearDown(self):
        self.database.close()