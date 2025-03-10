from fastapi import APIRouter, UploadFile, File, HTTPException
from app.loader_factory import LoaderFactory
from repository.article_repository import ArticleRepository

router = APIRouter()
article_repository = ArticleRepository()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a document and adds it to the vector store.
    """
    try:
        # Save file temporarily
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Load & process document
        loader = LoaderFactory.create_loader("pdf", file_path=file_path)
        docs = loader.load()
        doc_splits = article_repository.splitter.split(docs)
        document_ids = article_repository.add(doc_splits)

        return {"message": "Document uploaded successfully", "document_ids": document_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
