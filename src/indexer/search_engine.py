class SearchEngine:
    def __init__(self, indexer):
        self.indexer = indexer

    def search(self, query):
        results = []
        for document in self.indexer.get_all_documents():
            if self._matches_query(document, query):
                results.append(document)
        return results

    def _matches_query(self, document, query):
        return query.lower() in document.title.lower() or query.lower() in document.content.lower()