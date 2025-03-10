"""
tiktoken_spliter.py
-------------------
Implements a document splitter using the Tiktoken encoder.
This splitter is useful for breaking large documents into smaller chunks while 
preserving context for retrieval-augmented generation (RAG).
"""

import logging
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.base_spliter import BaseSpliter


class TiktokenSpliter(BaseSpliter):
    """
    Document splitter using Tiktoken encoding.

    This class is responsible for splitting long documents into smaller 
    chunks for efficient vector storage and retrieval.

    Methods:
        split(docs: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
            Splits documents into smaller chunks while maintaining context.
    """

    def split(self, docs: List[Document], chunk_size: int = 250, chunk_overlap: int = 0) -> List[Document]:
        """
        Splits a list of documents into smaller chunks using the Tiktoken encoder.

        Args:
            docs (List[Document]): The list of documents to split.
            chunk_size (int, optional): The size of each chunk in characters. Defaults to 250.
            chunk_overlap (int, optional): Number of overlapping characters between chunks. Defaults to 0.

        Returns:
            List[Document]: A list of smaller document chunks.
        """
        if not docs:
            logging.warning("No documents provided for splitting.")
            return []

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return text_splitter.split_documents(docs)
