"""
Document API routes for knowledge base management
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.services.document_service import DocumentService

router = APIRouter()


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    chunks_processed: int
    metadata: Dict[str, Any]


class DocumentSearchRequest(BaseModel):
    query: str
    limit: int = 10
    similarity_threshold: float = 0.7


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    metadata: Dict[str, Any]
    created_at: str


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    document_service: DocumentService = Depends(lambda: None)
):
    """
    Upload and process a document for the knowledge base
    """
    try:
        if not document_service:
            raise HTTPException(status_code=503, detail="Document service not available")
        
        result = await document_service.process_document(
            file=file,
            background_tasks=background_tasks
        )
        
        return DocumentUploadResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    limit: int = Query(50, ge=1, le=100),
    document_service: DocumentService = Depends(lambda: None)
):
    """
    List all documents in the knowledge base
    """
    try:
        if not document_service:
            raise HTTPException(status_code=503, detail="Document service not available")
        
        documents = await document_service.list_documents(limit)
        
        return [
            DocumentResponse(
                document_id=doc_id,
                filename=doc.get("filename", "Unknown"),
                metadata=doc,
                created_at=doc.get("uploaded_at", "")
            )
            for doc_id, doc in enumerate(documents)
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    document_service: DocumentService = Depends(lambda: None)
):
    """
    Get document metadata by ID
    """
    try:
        if not document_service:
            raise HTTPException(status_code=503, detail="Document service not available")
        
        document = await document_service.get_document(document_id)
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return DocumentResponse(
            document_id=document_id,
            filename=document.get("filename", "Unknown"),
            metadata=document,
            created_at=document.get("uploaded_at", "")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(lambda: None)
):
    """
    Delete a document from the knowledge base
    """
    try:
        if not document_service:
            raise HTTPException(status_code=503, detail="Document service not available")
        
        success = await document_service.delete_document(document_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "message": "Document deleted successfully",
            "document_id": document_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def search_documents(
    request: DocumentSearchRequest,
    document_service: DocumentService = Depends(lambda: None)
):
    """
    Search documents by content
    """
    try:
        if not document_service:
            raise HTTPException(status_code=503, detail="Document service not available")
        
        results = await document_service.search_documents(
            query=request.query,
            limit=request.limit
        )
        
        return {
            "query": request.query,
            "results": results,
            "total_found": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/semantic")
async def semantic_search(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    similarity_threshold: float = Query(0.7, ge=0.0, le=1.0),
    document_service: DocumentService = Depends(lambda: None)
):
    """
    Perform semantic search across documents
    """
    try:
        if not document_service:
            raise HTTPException(status_code=503, detail="Document service not available")
        
        results = await document_service.search_documents(
            query=query,
            limit=limit
        )
        
        return {
            "query": query,
            "results": results,
            "total_found": len(results),
            "similarity_threshold": similarity_threshold
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics/overview")
async def get_document_statistics(
    document_service: DocumentService = Depends(lambda: None)
):
    """
    Get document processing statistics
    """
    try:
        if not document_service:
            raise HTTPException(status_code=503, detail="Document service not available")
        
        stats = await document_service.get_document_statistics()
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-upload")
async def batch_upload_documents(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None,
    document_service: DocumentService = Depends(lambda: None)
):
    """
    Upload multiple documents at once
    """
    try:
        if not document_service:
            raise HTTPException(status_code=503, detail="Document service not available")
        
        if len(files) > 10:  # Limit batch size
            raise HTTPException(status_code=400, detail="Maximum 10 files per batch")
        
        results = []
        for file in files:
            try:
                result = await document_service.process_document(
                    file=file,
                    background_tasks=background_tasks
                )
                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "total_files": len(files),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"]),
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

