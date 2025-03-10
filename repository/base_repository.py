"""
base_repository.py
------------------
Defines an abstract base class for loaders.
Each repository is responsible for loading documents and returning them 
in a structured format.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    """
    Abstract base class for document loaders.

    Each repository subclass must implement a method to add and manage documents.

    Methods:
        add(data: Any) -> None: Abstract method to be implemented for adding documents.
    """

    @abstractmethod
    def add(self, data: Any) -> None:
        """
        Adds a document or dataset to the repository.

        Args:
            data (Any): The data to be added to the repository. The exact format depends on the implementation.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass
