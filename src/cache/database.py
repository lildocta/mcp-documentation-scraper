class Database:
    def __init__(self, db_name='documents.db'):
        import sqlite3
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        self.connection.commit()

    def store_document(self, title, content, metadata=None):
        self.cursor.execute('''
            INSERT INTO documents (title, content, metadata)
            VALUES (?, ?, ?)
        ''', (title, content, metadata))
        self.connection.commit()

    def retrieve_document(self, doc_id):
        self.cursor.execute('''
            SELECT * FROM documents WHERE id = ?
        ''', (doc_id,))
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()