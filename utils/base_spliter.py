"""
base_spliter.py
---------------
Defines an abstract base class for document splitters.
Each splitter implementation must handle document chunking for efficient processing.
"""

from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document


class BaseSpliter(ABC):
    """
    Abstract base class for document splitters.

    A document splitter is responsible for breaking down long documents into 
    smaller chunks to facilitate retrieval-augmented generation (RAG) and vector storage.

    Methods:
        split(docs: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
            Splits documents into smaller chunks while maintaining context.
    """

    @abstractmethod
    def split(self, docs: List[Document], chunk_size: int = 250, chunk_overlap: int = 0) -> List[Document]:
        """
        Splits a list of documents into smaller chunks.

        Args:
            docs (List[Document]): The list of documents to split.
            chunk_size (int, optional): The size of each chunk in characters. Defaults to 250.
            chunk_overlap (int, optional): Number of overlapping characters between chunks. Defaults to 0.

        Returns:
            List[Document]: A list of smaller document chunks.
        """
        pass
