"""
Document Service for handling document ingestion and processing
Supports multiple file formats and cloud storage integration
"""

import asyncio
import logging
import os
import uuid
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path
import mimetypes

from fastapi import UploadFile
from langchain.document_loaders import (
    PyPDFLoader, TextLoader, Docx2txtLoader, 
    UnstructuredHTMLLoader, CSVLoader, JSONLoader
)
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import aiofiles

from app.core.config import settings
from app.services.rag_service import RAGService
from app.core.cloud_storage import CloudStorageManager

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document processing and management"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
        self.storage_manager = CloudStorageManager()
        self.rag_service = None
        self.document_metadata = {}
        
    async def initialize(self, rag_service: RAGService = None):
        """Initialize the document service"""
        try:
            logger.info("Initializing Document service...")
            
            self.rag_service = rag_service
            
            # Create document storage directory
            os.makedirs(settings.DOCUMENT_STORAGE_PATH, exist_ok=True)
            
            # Initialize cloud storage if configured
            await self.storage_manager.initialize()
            
            logger.info("✅ Document service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Document service: {str(e)}")
            raise
    
    async def process_document(
        self,
        file: UploadFile,
        background_tasks = None
    ) -> Dict[str, Any]:
        """Process uploaded document and add to knowledge base"""
        try:
            # Validate file
            if not self._validate_file(file):
                raise ValueError("Invalid file type or size")
            
            # Generate unique document ID
            document_id = str(uuid.uuid4())
            
            # Save file locally
            file_path = await self._save_file(file, document_id)
            
            # Process document
            documents = await self._load_documents(file_path, file.filename)
            
            # Extract metadata
            metadata = await self._extract_metadata(file, documents)
            
            # Store metadata
            self.document_metadata[document_id] = metadata
            
            # Add to RAG service if available
            if self.rag_service:
                await self.rag_service.add_documents(documents)
            
            # Upload to cloud storage if configured
            if background_tasks and settings.AWS_S3_BUCKET:
                background_tasks.add_task(
                    self._upload_to_cloud,
                    document_id,
                    file_path,
                    file.filename
                )
            
            return {
                "document_id": document_id,
                "filename": file.filename,
                "status": "processed",
                "chunks_processed": len(documents),
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise
    
    def _validate_file(self, file: UploadFile) -> bool:
        """Validate uploaded file"""
        try:
            # Check file size
            if file.size and file.size > settings.MAX_FILE_SIZE:
                logger.warning(f"File too large: {file.size} bytes")
                return False
            
            # Check file extension
            if file.filename:
                file_ext = Path(file.filename).suffix.lower()
                if file_ext not in settings.SUPPORTED_FILE_TYPES:
                    logger.warning(f"Unsupported file type: {file_ext}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return False
    
    async def _save_file(self, file: UploadFile, document_id: str) -> str:
        """Save uploaded file to local storage"""
        try:
            file_ext = Path(file.filename).suffix if file.filename else ""
            file_path = Path(settings.DOCUMENT_STORAGE_PATH) / f"{document_id}{file_ext}"
            
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            logger.info(f"Saved file: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise
    
    async def _load_documents(self, file_path: str, filename: str) -> List[Document]:
        """Load documents using appropriate loader"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            # Select appropriate loader
            if file_ext == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_ext == '.docx':
                loader = Docx2txtLoader(file_path)
            elif file_ext == '.html':
                loader = UnstructuredHTMLLoader(file_path)
            elif file_ext == '.csv':
                loader = CSVLoader(file_path)
            elif file_ext == '.json':
                loader = JSONLoader(file_path)
            else:
                # Fallback to text loader
                loader = TextLoader(file_path, encoding='utf-8')
            
            # Load documents
            documents = await asyncio.get_event_loop().run_in_executor(
                None, loader.load
            )
            
            # Add metadata to documents
            for doc in documents:
                doc.metadata.update({
                    "source": filename,
                    "file_path": file_path,
                    "processed_at": datetime.utcnow().isoformat(),
                    "file_type": file_ext
                })
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            logger.info(f"Loaded {len(chunks)} chunks from {filename}")
            return chunks
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            raise
    
    async def _extract_metadata(self, file: UploadFile, documents: List[Document]) -> Dict[str, Any]:
        """Extract metadata from document"""
        try:
            # Basic file metadata
            metadata = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size,
                "uploaded_at": datetime.utcnow().isoformat(),
                "total_chunks": len(documents),
                "total_characters": sum(len(doc.page_content) for doc in documents)
            }
            
            # Extract content metadata
            if documents:
                content_sample = documents[0].page_content[:500]
                metadata.update({
                    "has_content": True,
                    "content_preview": content_sample,
                    "first_chunk_size": len(documents[0].page_content)
                })
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}")
            return {"error": str(e)}
    
    async def _upload_to_cloud(self, document_id: str, file_path: str, filename: str):
        """Upload document to cloud storage"""
        try:
            cloud_url = await self.storage_manager.upload_file(
                file_path=file_path,
                object_name=f"documents/{document_id}/{filename}"
            )
            
            # Update metadata with cloud URL
            if document_id in self.document_metadata:
                self.document_metadata[document_id]["cloud_url"] = cloud_url
            
            logger.info(f"Uploaded to cloud: {cloud_url}")
            
        except Exception as e:
            logger.error(f"Error uploading to cloud: {str(e)}")
    
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get document metadata"""
        return self.document_metadata.get(document_id)
    
    async def list_documents(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List all documents"""
        try:
            documents = list(self.document_metadata.values())
            return documents[-limit:] if limit else documents
            
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            return []
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete document and remove from knowledge base"""
        try:
            if document_id not in self.document_metadata:
                return False
            
            metadata = self.document_metadata[document_id]
            
            # Delete local file
            if "file_path" in metadata:
                file_path = metadata["file_path"]
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Delete from cloud storage
            if "cloud_url" in metadata:
                await self.storage_manager.delete_file(metadata["cloud_url"])
            
            # Remove from metadata
            del self.document_metadata[document_id]
            
            # Note: Removing from vector store would require additional implementation
            
            logger.info(f"Deleted document: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search documents by content"""
        try:
            # This would integrate with the RAG service for semantic search
            if self.rag_service:
                results = await self.rag_service.search_documents(query, limit)
                return results
            
            # Fallback to simple text search
            results = []
            for doc_id, metadata in self.document_metadata.items():
                if query.lower() in metadata.get("content_preview", "").lower():
                    results.append({
                        "document_id": doc_id,
                        "metadata": metadata,
                        "relevance": "medium"
                    })
            
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    async def get_document_statistics(self) -> Dict[str, Any]:
        """Get document processing statistics"""
        try:
            total_docs = len(self.document_metadata)
            total_chunks = sum(
                meta.get("total_chunks", 0) 
                for meta in self.document_metadata.values()
            )
            total_size = sum(
                meta.get("size", 0) 
                for meta in self.document_metadata.values()
            )
            
            file_types = {}
            for meta in self.document_metadata.values():
                filename = meta.get("filename", "")
                ext = Path(filename).suffix.lower()
                file_types[ext] = file_types.get(ext, 0) + 1
            
            return {
                "total_documents": total_docs,
                "total_chunks": total_chunks,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "file_types": file_types,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting document statistics: {str(e)}")
            return {}


class CloudStorageManager:
    """Manager for cloud storage operations"""
    
    def __init__(self):
        self.s3_client = None
        self.azure_client = None
        self.gcp_client = None
        
    async def initialize(self):
        """Initialize cloud storage clients"""
        try:
            # Initialize AWS S3
            if settings.AWS_ACCESS_KEY_ID and settings.AWS_S3_BUCKET:
                import boto3
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION
                )
            
            # Initialize Azure Blob Storage
            if settings.AZURE_STORAGE_CONNECTION_STRING:
                from azure.storage.blob import BlobServiceClient
                self.azure_client = BlobServiceClient.from_connection_string(
                    settings.AZURE_STORAGE_CONNECTION_STRING
                )
            
            # Initialize Google Cloud Storage
            if settings.GCP_PROJECT_ID and settings.GCP_BUCKET_NAME:
                from google.cloud import storage
                self.gcp_client = storage.Client(project=settings.GCP_PROJECT_ID)
                
        except Exception as e:
            logger.error(f"Error initializing cloud storage: {str(e)}")
    
    async def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload file to cloud storage"""
        try:
            if self.s3_client:
                return await self._upload_to_s3(file_path, object_name)
            elif self.azure_client:
                return await self._upload_to_azure(file_path, object_name)
            elif self.gcp_client:
                return await self._upload_to_gcp(file_path, object_name)
            else:
                raise ValueError("No cloud storage configured")
                
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise
    
    async def _upload_to_s3(self, file_path: str, object_name: str) -> str:
        """Upload to AWS S3"""
        try:
            self.s3_client.upload_file(
                file_path,
                settings.AWS_S3_BUCKET,
                object_name
            )
            return f"s3://{settings.AWS_S3_BUCKET}/{object_name}"
        except Exception as e:
            raise Exception(f"S3 upload failed: {str(e)}")
    
    async def _upload_to_azure(self, file_path: str, object_name: str) -> str:
        """Upload to Azure Blob Storage"""
        try:
            blob_client = self.azure_client.get_blob_client(
                container=settings.AZURE_CONTAINER_NAME,
                blob=object_name
            )
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            return blob_client.url
        except Exception as e:
            raise Exception(f"Azure upload failed: {str(e)}")
    
    async def _upload_to_gcp(self, file_path: str, object_name: str) -> str:
        """Upload to Google Cloud Storage"""
        try:
            bucket = self.gcp_client.bucket(settings.GCP_BUCKET_NAME)
            blob = bucket.blob(object_name)
            blob.upload_from_filename(file_path)
            return f"gs://{settings.GCP_BUCKET_NAME}/{object_name}"
        except Exception as e:
            raise Exception(f"GCP upload failed: {str(e)}")
    
    async def delete_file(self, cloud_url: str) -> bool:
        """Delete file from cloud storage"""
        try:
            if cloud_url.startswith("s3://"):
                # Parse S3 URL and delete
                parts = cloud_url[5:].split("/", 1)
                bucket = parts[0]
                key = parts[1]
                self.s3_client.delete_object(Bucket=bucket, Key=key)
            elif "blob.core.windows.net" in cloud_url:
                # Parse Azure URL and delete
                blob_client = self.azure_client.get_blob_client(
                    container=settings.AZURE_CONTAINER_NAME,
                    blob=cloud_url.split("/")[-1]
                )
                blob_client.delete_blob()
            elif cloud_url.startswith("gs://"):
                # Parse GCP URL and delete
                parts = cloud_url[5:].split("/", 1)
                bucket_name = parts[0]
                object_name = parts[1]
                bucket = self.gcp_client.bucket(bucket_name)
                blob = bucket.blob(object_name)
                blob.delete()
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting cloud file: {str(e)}")
            return False

