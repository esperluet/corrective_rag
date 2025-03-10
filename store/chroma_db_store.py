import logging
from typing import List, Optional
from langchain.schema import Document
from store.base_store import BaseStore
from langchain_chroma import Chroma
from utils.id_utils import generate_list_ids


class ChromaDBStore(BaseStore):
    """
    Implements a ChromaDB vector store for document storage and retrieval.

    Attributes:
        collection_name (str): Name of the collection in ChromaDB.
        embeddings: Embedding function used for vector storage.
        persist_directory (str): Directory where ChromaDB stores persistent data.
        vector_store (Chroma): The Chroma vector database instance.
    """

    def __init__(self, collection_name: str, embeddings, persist_directory: str = "./chroma_langchain_db"):
        """
        Initializes the ChromaDB vector store.

        Args:
            collection_name (str): The name of the collection in ChromaDB.
            embeddings: Embedding function for document vectorization.
            persist_directory (str, optional): Directory for ChromaDB persistence. Defaults to "./chroma_langchain_db".
        """
        self.collection_name = collection_name
        self.embeddings = embeddings
        self.persist_directory = persist_directory

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def get_vector_store(self) -> Chroma:
        """
        Returns the underlying ChromaDB vector store instance.

        Returns:
            Chroma: The Chroma vector store object.
        """
        return self.vector_store

    def add_documents(self, documents: List[Document]) -> Optional[List[str]]:
        """
        Adds a list of documents to the ChromaDB vector store.

        Args:
            documents (List[Document]): A list of LangChain Document objects.

        Returns:
            Optional[List[str]]: List of document IDs if successful, None otherwise.
        """
        uuids = generate_list_ids(len(documents))

        try:
            return self.vector_store.add_documents(documents=documents, ids=uuids)
        except ValueError as e:
            logging.error(f"Error saving documents to ChromaDB: {e}")
            return None

    def similarity_search(self, query: str, count: int = 4) -> List[Document]:
        """
        Performs a similarity search based on a text query.

        Args:
            query (str): The text query for retrieving similar documents.
            count (int, optional): Number of documents to retrieve. Defaults to 4.

        Returns:
            List[Document]: A list of retrieved documents.
        """
        return self.vector_store.similarity_search(query, k=count)

    def similarity_search_by_vector(self, query: str, count: int = 4) -> List[Document]:
        """
        Performs a similarity search using an embedding-based query.

        Args:
            query (str): The query string, which will be converted into a vector.
            count (int, optional): Number of documents to retrieve. Defaults to 4.

        Returns:
            List[Document]: A list of retrieved documents.
        """
        return self.vector_store.similarity_search_by_vector(
            embedding=self.embeddings.embed_query(query),
            k=count
        )
