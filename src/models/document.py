class Document:
    def __init__(self, doc_id, title, content, metadata=None):
        self.id = doc_id
        self.title = title
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"Document(id={self.id}, title={self.title}, content_length={len(self.content)}, metadata={self.metadata})"