import os
import json
from typing import List, Dict, Any

class DocumentIndexer:
    def __init__(self):
        self.index_file = os.path.join(os.getcwd(), "cache", "document_index.json")
        self._ensure_index_file()

    def _ensure_index_file(self):
        """Ensure the index file exists"""
        os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
        if not os.path.exists(self.index_file):
            with open(self.index_file, 'w') as f:
                json.dump([], f)

    def index_document(self, data: Dict[str, Any]):
        """Index a document"""
        try:
            # Load existing index
            with open(self.index_file, 'r') as f:
                index = json.load(f)
            
            # Create document entry
            doc_entry = {
                'url': data.get('url', ''),
                'title': data.get('title', ''),
                'content': data.get('content', ''),
                'summary': data.get('summary', ''),
                'indexed_at': data.get('indexed_at', str(json.dumps({})))
            }
            
            # Remove any existing entry with the same URL
            index = [doc for doc in index if doc.get('url') != data.get('url')]
            
            # Add new entry
            index.append(doc_entry)
            
            # Save index
            with open(self.index_file, 'w') as f:
                json.dump(index, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error indexing document: {e}")
            return False

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search through indexed documents"""
        try:
            # Load index
            with open(self.index_file, 'r') as f:
                index = json.load(f)
            
            # Simple text search (can be improved with better search later)
            query_lower = query.lower()
            results = []
            
            for doc in index:
                score = 0
                title = doc.get('title', '').lower()
                content = doc.get('content', '').lower()
                
                # Simple scoring: title matches count more
                if query_lower in title:
                    score += 3
                if query_lower in content:
                    score += 1
                
                if score > 0:
                    doc_result = doc.copy()
                    doc_result['score'] = score
                    results.append(doc_result)
            
            # Sort by score and limit results
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:max_results]
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []

    def update_document(self, document_id, data):
        """Update a document (placeholder)"""
        pass

    def delete_document(self, document_id):
        """Delete a document (placeholder)"""
        pass

    def get_document(self, document_id):
        """Get a document (placeholder)"""
        return None
    
    def is_healthy(self) -> bool:
        """Check if the indexer is healthy"""
        try:
            return os.path.exists(self.index_file)
        except:
            return False