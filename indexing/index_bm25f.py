from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.scoring import BM25F
from whoosh.analysis import SpaceSeparatedTokenizer
import os

class IndexBM25F:
    """Define methods to initialize and update BM25F index.
    """

    def __init__(self):
        analyzer = SpaceSeparatedTokenizer()
        schema = Schema(
            id = ID(stored = True, unique = True),
            title = TEXT(stored = True, analyzer = analyzer, field_boost = 2.0),
            abstract = TEXT(stored = True, analyzer = analyzer, field_boost = 2.5),
            authors = TEXT(stored = True, analyzer = analyzer),
            content = TEXT(stored = False,  analyzer = analyzer),
            pdf_hash = STORED()
        )
        index_path = os.path.join("indexing", "index_dir")
        if not os.path.exists(index_path):
            os.mkdir(index_path)
            create_in(index_path, schema)

    def add_document(self, datos_paper: dict):
        """Add document to index.
        """

        index_path = os.path.join("indexing", "index_dir")
        ix = open_dir(index_path)
        writer = ix.writer()
        writer.add_document(
            id = str(datos_paper['id']),
            title = str(datos_paper['title']).encode('utf-8', 'ignore').decode('utf-8'),
            abstract = str(datos_paper['abstract']).encode('utf-8', 'ignore').decode('utf-8'),
            authors = str(datos_paper['authors']).encode('utf-8', 'ignore').decode('utf-8'),
            content = str(datos_paper['text']).encode('utf-8', 'ignore').decode('utf-8'),
            pdf_hash = str(datos_paper['pdf_hash']).encode('utf-8', 'ignore').decode('utf-8')
        )
        writer.commit()