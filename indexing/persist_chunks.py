import sqlite3
from typing import Dict, Optional
import os

class PersistChunk:
    """
    Example: \n
    pc = PersistChunk() \n
    sample_data = { 
        'chunk_hash': 'asd123', 
        'pdf_hash': 'zxc123', 
        'title': 'ABC', 
        'content': 'abc...' 
    } \n
    pc.persist_chunk(sample_data) \n
    pc.get_chunk_by_hash('asd123')
    """

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DB_NAME = os.path.join(self.BASE_DIR, "docusearch.db")
        self.init_db()
        
    def init_db(self):
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_hash TEXT PRIMARY KEY,
                    pdf_hash TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_chunk_hash ON chunks (chunk_hash)')
            conn.commit()

    def persist_chunk(self, data: Dict[str, str]):
        query = '''
            INSERT OR REPLACE INTO chunks (chunk_hash, pdf_hash, title, content)
            VALUES (:chunk_hash, :pdf_hash, :title, :content)
        '''
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, data)
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error while persisting chunk: {e}")

    def get_chunk_by_hash(self, chunk_hash: str) -> Optional[Dict[str, str]]:
        query = 'SELECT chunk_hash, pdf_hash, title, content FROM chunks WHERE chunk_hash = ?'
        with sqlite3.connect(self.DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (chunk_hash,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        
    def get_title_by_pdf_hash(self, pdf_hash: str) -> Optional[str]:
        query = 'SELECT title FROM chunks WHERE pdf_hash = ? LIMIT 1'
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (pdf_hash,))
            row = cursor.fetchone()
            return row[0] if row else None