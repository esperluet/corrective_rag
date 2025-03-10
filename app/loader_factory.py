"""
loader_factory.py
-----------------
Defines the LoaderFactory class for creating document loaders (URL, PDF, etc.).
"""

import logging
from retrieval.url_loader import URLLoader
from retrieval.pdf_loader import PDFLoader
from retrieval.base_loader import BaseLoader


class LoaderFactory:
    """
    Factory class for creating different types of document loaders.
    """

    @staticmethod
    def create_loader(source_type: str, **kwargs) -> BaseLoader:
        """
        Creates a document loader based on the source type (URL, PDF, etc.).

        Args:
            source_type (str): The type of source ("url", "pdf", etc.).
            **kwargs: Additional parameters required for loader initialization.

        Returns:
            BaseLoader: An instance of the appropriate document loader.

        Raises:
            ValueError: If the source type is unknown or required parameters are missing.
        """
        if source_type == "url":
            urls = kwargs.get("urls")
            if not urls:
                raise ValueError("Missing required parameter: 'urls' must be provided for URLLoader.")
            return URLLoader(urls)

        elif source_type == "pdf":
            file_path = kwargs.get("file_path")
            if not file_path:
                raise ValueError("Missing required parameter: 'file_path' must be provided for PDFLoader.")
            return PDFLoader(file_path)

        # elif source_type == "ppt": ...
        # elif source_type == "img": ...

        else:
            logging.error(f"Unknown source type requested: {source_type}")
            raise ValueError(f"Unknown source type: {source_type}")
