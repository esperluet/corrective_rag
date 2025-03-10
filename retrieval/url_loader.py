import logging
from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import Document
from .base_loader import BaseLoader


class URLLoader(BaseLoader):
    """
    Loads documents from a list of URLs using WebBaseLoader.

    Attributes:
        urls (List[str]): List of URLs to fetch content from.
    """

    def __init__(self, urls: List[str]):
        """
        Initializes the URLLoader with a list of URLs.

        Args:
            urls (List[str]): List of URLs to fetch content from.
        """
        super().__init__()  # Ensures proper inheritance from BaseLoader
        self.urls = urls

    def load(self) -> List[Document]:
        """
        Loads documents from the given URLs.

        Returns:
            List[Document]: A list of LangChain Document objects retrieved from the web.

        Raises:
            ValueError: If no URLs are provided.
            Exception: Logs any errors encountered during document loading.
        """
        if not self.urls:
            raise ValueError("No URLs provided for loading.")

        try:
            loader = WebBaseLoader(self.urls)
            return loader.load()
        except Exception as e:
            logging.error(f"Error loading documents from URLs: {e}")
            return []
