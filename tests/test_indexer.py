import unittest
from src.indexer.document_indexer import DocumentIndexer
from src.indexer.search_engine import SearchEngine

class TestDocumentIndexer(unittest.TestCase):
    def setUp(self):
        self.indexer = DocumentIndexer()
        self.test_data = {
            'id': '1',
            'title': 'Test Document',
            'content': 'This is a test document for indexing.',
            'metadata': {'author': 'Test Author'}
        }

    def test_index_document(self):
        result = self.indexer.index_document(self.test_data)
        self.assertTrue(result)
        # Additional assertions can be added to verify the indexed data

class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        self.indexer = DocumentIndexer()
        self.search_engine = SearchEngine(self.indexer)
        self.test_data = {
            'id': '1',
            'title': 'Test Document',
            'content': 'This is a test document for indexing.',
            'metadata': {'author': 'Test Author'}
        }
        self.indexer.index_document(self.test_data)

    def test_search(self):
        results = self.search_engine.search('test')
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['title'], 'Test Document')

if __name__ == '__main__':
    unittest.main()