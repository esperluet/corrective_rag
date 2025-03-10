from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.loader_factory import LoaderFactory
from repository.article_repository import ArticleRepository
from utils.tiktoken_spliter import TiktokenSpliter

router = APIRouter()
article_repository = ArticleRepository()
splitter = TiktokenSpliter()

class URLInput(BaseModel):
    urls: List[str]

@router.post("/add-url")
def add_documents_from_url(data: URLInput):
    """
    Adds documents from URLs to the vector store.
    """
    try:
        loader = LoaderFactory.create_loader("url", urls=data.urls)
        docs = loader.load()
        doc_splits = splitter.split(docs)
        document_ids = article_repository.add(doc_splits)
        return {"message": "Documents added successfully", "document_ids": document_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
