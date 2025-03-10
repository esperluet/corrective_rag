from typing import List, Optional
from langchain.schema import Document
from repository.base_repository import BaseRepository
from store.chroma_db_store import ChromaDBStore
from langchain_ollama import OllamaEmbeddings


class ArticleRepository(BaseRepository):
    """
    Repository class for managing articles in a vector store.

    This class provides methods to add, retrieve, update, and delete articles
    stored in a ChromaDB vector database.

    Attributes:
        embeddings (OllamaEmbeddings): Embedding model used for vector storage.
        collection_name (str): Name of the collection in ChromaDB.
        vector_store: Vector database instance.
        store_instance: Store instance handling vector operations.
    """

    def __init__(self, embeddings: Optional[OllamaEmbeddings] = None, persist_directory: str = "./chroma_langchain_db"):
        """
        Initializes the ArticleRepository with an embedding model and a ChromaDB store.

        Args:
            embeddings (Optional[OllamaEmbeddings], optional): Embedding model. Defaults to "all-minilm" if not provided.
            persist_directory (str, optional): Directory for ChromaDB persistence. Defaults to "./chroma_langchain_db".
        """
        self.embeddings = embeddings if embeddings else OllamaEmbeddings(model="all-minilm")
        self.collection_name = "articles"

        chroma_store = ChromaDBStore(
            collection_name=self.collection_name,
            embeddings=self.embeddings,
            persist_directory=persist_directory,
        )
        self.vector_store = chroma_store.get_vector_store()
        self.store_instance = chroma_store

    def add(self, documents: List[Document]) -> List[str]:
        """
        Adds documents to the ChromaDB vector store.

        Args:
            documents (List[Document]): A list of LangChain Document objects to store.

        Returns:
            List[str]: List of document IDs that were successfully added.
        """
        return self.store_instance.add_documents(documents)

    def delete(self, ids: List[str]) -> None:
        """
        Deletes documents from the vector store by their IDs.

        Args:
            ids (List[str]): List of document IDs to delete.
        """
        pass

    def update(self, ids: List[str]) -> None:
        """
        Updates documents in the vector store.

        Args:
            ids (List[str]): List of document IDs to update.
        """
        pass

    def retrieve(self, query: str, count: int = 4) -> List[Document]:
        """
        Retrieves the most relevant documents based on similarity search.

        Args:
            query (str): The query text for document retrieval.
            count (int, optional): Number of documents to retrieve. Defaults to 4.

        Returns:
            List[Document]: A list of retrieved documents.
        """
        return self.store_instance.similarity_search_by_vector(query, count)
