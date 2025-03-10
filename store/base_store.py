"""
base_store.py
-------------
Defines an abstract base class for vector stores.
Each store implementation must handle document storage, retrieval, and similarity search.
"""

from abc import ABC, abstractmethod
from typing import List, Any
from langchain.schema import Document


class BaseStore(ABC):
    """
    Abstract base class for vector stores.

    This class defines methods for storing, retrieving, and searching documents 
    in a vector-based storage system.

    Methods:
        get_vector_store() -> Any:
            Returns the underlying vector store instance.
        
        add_documents(documents: List[Document]) -> List[str]:
            Adds documents to the store and returns their unique IDs.
        
        similarity_search(query: str, count: int = 4) -> List[Document]:
            Performs a similarity search based on text queries.
        
        similarity_search_by_vector(query: str, count: int = 4) -> List[Document]:
            Performs a similarity search based on embeddings.
    """

    @abstractmethod
    def get_vector_store(self) -> Any:
        """
        Returns the underlying vector store instance.

        Returns:
            Any: The vector store object (e.g., ChromaDB, FAISS).
        """
        pass

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Adds a list of documents to the vector store.

        Args:
            documents (List[Document]): A list of LangChain Document objects to be stored.

        Returns:
            List[str]: A list of document IDs that were successfully added.
        """
        pass

    @abstractmethod
    def similarity_search(self, query: str, count: int = 4) -> List[Document]:
        """
        Performs a similarity search based on a text query.

        Args:
            query (str): The text query to search for.
            count (int, optional): Number of documents to retrieve. Defaults to 4.

        Returns:
            List[Document]: A list of retrieved documents.
        """
        pass

    @abstractmethod
    def similarity_search_by_vector(self, query: str, count: int = 4) -> List[Document]:
        """
        Performs a similarity search using a vector-based query.

        Args:
            query (str): The vector representation of the query.
            count (int, optional): Number of documents to retrieve. Defaults to 4.

        Returns:
            List[Document]: A list of retrieved documents.
        """
        pass
