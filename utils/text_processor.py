import re
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os

nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
nltk.data.path.insert(0, nltk_data_path)

def chunking(tokens: list[str], chunk_size = 500, overlap = 100) -> list[list[str]]:
    """Divides list of tokens in chunks. A chunk contains 'chunk_size' tokens, 'overlap' of which overlap with the previous chunk.

    Args:
        tokens (list[str]): list of tokens
        chunk_size (int, optional): Max size of the chunk. Defaults to 500.
        overlap (int, optional): overlapping size. Defaults to 100.

    Returns:
        list[list[str]]: list of chunks, a chunk is a list of tokens.
    """

    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(tokens[i : i + chunk_size])
    return chunks

class TextPreprocessor:
    """Remove citations -> tokenize -> remove stop words -> stemming
    """

    def __init__(self, text: str):

        self.text = text
        self.tokens = []

    def clear_text(self) -> str:
        """Clear surrogate characters.
        """

        return self.text.encode('utf-8', 'ignore').decode('utf-8')

    def _remove_citations(self) -> str:
        """Remove citations from a text.
        """

        pattern = "\[[\d\s,.\-]+\]"
        return re.sub(pattern, '', self.text)

    def _tokenize(self) -> list[str]:
        """Tokenize text.
        """

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.text)
        tokens = []
        for token in doc:
            if token.text.isalpha():
                tokens.append(token.lemma_)
        return tokens

    def _remove_stop_words(self) -> list[str]:
        """Remove the english stop words.
        """

        stop_words = set(stopwords.words('english'))
        return [word for word in self.tokens if word not in stop_words]

    def _stemming(self) -> list[str]:
        """Reduce words to their stem.
        """

        stemmer = SnowballStemmer('english')
        return [stemmer.stem(token) for token in self.tokens]
        
    def get_clean_text(self) -> str:
        self.text = self.text.lower()
        self.text = self.clear_text()
        self.text = self._remove_citations()
        return self.text
    
    def get_normalized_tokens(self, text = None) -> list[str]:
        """Normalize text and return tokens.
        """

        if text is not None:
            self.text = text
        self.text = self.get_clean_text()
        self.tokens = self._tokenize()
        self.tokens = self._remove_stop_words()
        self.tokens = self._stemming()
        return self.tokens