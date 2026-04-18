import re
import PyPDF2

class ExtractPdf:
    """Methods to extract data froma a PDF file. Title, Authors, Abstract, Text.
    """

    def __init__(self, path: str):
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            self.pages = reader.pages
            self.metadata = reader.metadata
            if self.metadata is None:
                self.metadata = {}
            self.text = ""
            for page in self.pages:
                self.text += page.extract_text() + "\n"

    def _get_abstract(text: str, length=500):
        """Extracts abstract from a given text.
        """

        text_lower = text.lower()
        pos_abstract = text_lower.find('abstract')
        pos_intro = text_lower.find('introduction')
        abstract_text = ""
        if pos_abstract != -1:
            text_from_abstract = text[pos_abstract:]
            prefix_pattern = r'^abstract[\s:.\n-]+'
            match = re.match(prefix_pattern, text_from_abstract, re.IGNORECASE)
            begins = pos_abstract + (len(match.group()) if match else len('abstract'))
            if pos_intro != -1 and pos_intro > begins:
                abstract_text = text[begins:pos_intro]
            else:
                abstract_text = text[begins:]
        elif pos_intro != -1:
            abstract_text = text[:pos_intro]
        if abstract_text:
            words = abstract_text.split()
            result = ' '.join(words[:length]).strip()
            return result
        return ""

    def _get_title(self) -> str:
        """Extracts title from the metadata of a PDF file.

        Returns:
            str: Title
        """

        return str(self.metadata.get('/Title', ''))

    def _get_authors(self) -> str:
        """Extracts authors from the metadata of a PDF file.

        Returns:
            str: Authors
        """

        return str(self.metadata.get('/Author', ''))

    def extract_pdf(self) -> dict:
        """Extracts text and metadata from a PDF file.

        Returns:
            dict: Authors, Title, Abstract, Text
        """

        return {
            'title': self._get_title(),
            'authors': self._get_authors(),
            'abstract': self._get_abstract(self.text),
            'text': self.text
        }