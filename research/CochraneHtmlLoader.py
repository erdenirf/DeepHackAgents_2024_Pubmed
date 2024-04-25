from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
import re

class CochraneHtmlLoader(BaseLoader):
    """Load from cochrane.org HTML file"""

    def __init__(self, file_path: str):
        """Initialize with filename

        Args:
            filename: The filename to open file.
        """
        self.filename: str = file_path
        self.page_content: str = ''
        self.metadata: str = ''
        self.id: str = None
        self.is_na = False

    def load(self, default: str = '', drop_na: bool = True) -> list[Document]:
        """Load documents."""
        try:
            from lxml import etree
        except ImportError:
            raise ImportError(
                "Could not import `lxml` python package. "
                "Please install it with `pip install lxml`."
            )
        with open(self.filename, 'r') as file:
            tree = etree.parse(file, parser=etree.HTMLParser())
            root = tree.getroot()
            citeDiv = root.find('.//div[@id="citation"]')
            citation = self._get_text_recursive(citeDiv)
            Plain_lang_summary = default
            div_summary = root.find('.//div[@class="field field-name-field-summary-body field-type-text-long field-label-hidden"]')
            if div_summary is None:
                div_protocol = root.find('.//div[@class="protocol-objective"]')
                if div_protocol is not None:
                    Plain_lang_summary = 'This is a protocol.'
                div_withdraw = root.find('.//div[@class="messages warning"]')
                if div_withdraw is not None:
                    Plain_lang_summary = 'This review has been withdrawn.'
                self.is_na = True
            else:
                for child1 in div_summary:
                    for child2 in child1:
                        for child3 in child2:
                            if not (child3.tag == 'div' and child3.attrib.get('class') == 'donate-box'):
                                Plain_lang_summary += self._get_text_recursive(child3) + '\n'
            self.page_content = Plain_lang_summary
            self.metadata = citation
            regular = re.search(r'((MR\d+)|(CD\d+))', citation)
            if regular:
                self.id = regular.group()
            if not self.is_na and len(self.page_content)>=100:
                return [Document(page_content=self.page_content, metadata={"source": self.metadata})]
            elif not drop_na and len(self.page_content)>=100:
                return [Document(page_content=self.page_content, metadata={"source": self.metadata})]
            return []
        
    def _get_text_recursive(self, element, separator: str = " ", default: str = '') -> str:
        if element is not None:
            return " ".join(separator.join(element.itertext()).strip().split())
        return default
    
    def _export_dict(self, drop_na: bool = True):
        if not self.is_na:
            return {
                "page_content": self.page_content,
                "metadata": self.metadata,
                "id": self.id,
            }
        elif not drop_na:
            return {
                "page_content": self.page_content,
                "metadata": self.metadata,
                "id": self.id,
            }
        else:
            return None