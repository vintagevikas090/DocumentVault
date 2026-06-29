import sqlite3
import os
from datetime import datetime

class DatabaseManager:

    def __init__(self, db_path="data/doc_inventory.db"):
        self.db_path = db_path
        self._initialize_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_path TEXT NOT NULL,
                    file_hash TEXT UNIQUE NOT NULL,
                    category TEXT DEFAULT 'Uncategorized',
                    added_date TEXT NOT NULL,
                    expiry_date TEXT,
                    file_size INTEGER
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_hash ON documents(file_hash)')
            conn.commit()

    def is_duplicate(self, file_hash: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM documents WHERE file_hash = ?", (file_hash,))
            return cursor.fetchone() is not None

    def insert_document(self, filename: str, original_path: str, file_hash: str, category: str, file_size: int, expiry_date: str = None) -> bool:
        """
        Insert a new document record into the database.
        Args:
            filename, original_path, file_hash , category , file_size , expiry_date 
        """
        try:
            added_date = datetime.now().isoformat()
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO documents (filename, original_path, file_hash, category, added_date, expiry_date, file_size)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (filename, original_path, file_hash, category, added_date, expiry_date, file_size))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_documents(self) -> list:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents")
            return [dict(row) for row in cursor.fetchall()]

    def search_documents(self, keyword: str = None, category: str = None) -> list:
        query = "SELECT * FROM documents WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND filename LIKE ?"
            params.append(f"%{keyword}%")
        
        if category:
            query += " AND category = ?"
            params.append(category)

        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def clear_database(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM documents")
            conn.commit()
