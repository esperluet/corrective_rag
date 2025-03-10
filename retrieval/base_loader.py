from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document

class BaseLoader(ABC):
    """
    Classe de base pour nos loaders. 
    Chaque loader est responsable de charger des documents et de les retourner
    sous forme de `List[Document]`.
    """

    @abstractmethod
    def load(self) -> List[Document]:
        pass
