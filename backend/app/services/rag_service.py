"""
RAG (Retrieval-Augmented Generation) Service
Combines document retrieval with LLM generation for accurate, contextual responses
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StreamingStdOutCallbackHandler

from app.core.config import settings, LLM_CONFIG, VECTOR_DB_CONFIG
from app.core.database import get_vector_store, get_conversation_memory

logger = logging.getLogger(__name__)


class RAGService:
    """RAG service for document retrieval and response generation"""
    
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.text_splitter = None
        self.qa_chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.conversation_sessions = {}
        
    async def initialize(self):
        """Initialize the RAG service components"""
        try:
            logger.info("Initializing RAG service...")
            
            # Initialize embeddings
            await self._initialize_embeddings()
            
            # Initialize vector store
            await self._initialize_vector_store()
            
            # Initialize LLM
            await self._initialize_llm()
            
            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
            )
            
            # Initialize QA chain
            await self._initialize_qa_chain()
            
            logger.info("✅ RAG service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG service: {str(e)}")
            raise
    
    async def _initialize_embeddings(self):
        """Initialize embedding model"""
        try:
            if settings.DEFAULT_LLM_PROVIDER == "openai":
                self.embeddings = OpenAIEmbeddings(
                    model=settings.EMBEDDING_MODEL,
                    openai_api_key=settings.OPENAI_API_KEY
                )
            else:
                # Fallback to sentence transformers
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer('all-MiniLM-L6-v2')
                self.embeddings = model
                
            logger.info(f"Embeddings initialized: {settings.EMBEDDING_MODEL}")
            
        except Exception as e:
            logger.error(f"Error initializing embeddings: {str(e)}")
            raise
    
    async def _initialize_vector_store(self):
        """Initialize vector database"""
        try:
            if settings.VECTOR_DB_TYPE == "chroma":
                self.vector_store = Chroma(
                    persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                    embedding_function=self.embeddings,
                    collection_name="documents"
                )
            elif settings.VECTOR_DB_TYPE == "faiss":
                import faiss
                # Create FAISS index if it doesn't exist
                self.vector_store = FAISS.load_local(
                    VECTOR_DB_CONFIG["faiss"]["index_path"],
                    self.embeddings
                ) if os.path.exists(VECTOR_DB_CONFIG["faiss"]["index_path"]) else None
                
            logger.info(f"Vector store initialized: {settings.VECTOR_DB_TYPE}")
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise
    
    async def _initialize_llm(self):
        """Initialize language model"""
        try:
            llm_config = LLM_CONFIG[settings.DEFAULT_LLM_PROVIDER]
            
            if settings.DEFAULT_LLM_PROVIDER == "openai":
                self.llm = ChatOpenAI(
                    model=llm_config["model"],
                    temperature=llm_config["temperature"],
                    max_tokens=llm_config["max_tokens"],
                    openai_api_key=llm_config["api_key"]
                )
            elif settings.DEFAULT_LLM_PROVIDER == "anthropic":
                from langchain_anthropic import ChatAnthropic
                self.llm = ChatAnthropic(
                    model=llm_config["model"],
                    temperature=llm_config["temperature"],
                    max_tokens=llm_config["max_tokens"],
                    anthropic_api_key=llm_config["api_key"]
                )
                
            logger.info(f"LLM initialized: {llm_config['model']}")
            
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            raise
    
    async def _initialize_qa_chain(self):
        """Initialize the QA chain with RAG"""
        try:
            if not self.vector_store:
                logger.warning("No vector store available, using LLM without RAG")
                return
                
            # Create prompt template
            prompt_template = """
            Use the following pieces of context to answer the user's question.
            If you don't know the answer based on the context, just say that you don't know.
            
            Context:
            {context}
            
            Question: {question}
            
            Chat History:
            {chat_history}
            
            Please provide a comprehensive and accurate answer:
            """
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question", "chat_history"]
            )
            
            # Create retrieval chain
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.TOP_K_RESULTS}
            )
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={
                    "prompt": PROMPT,
                    "memory": self.memory
                },
                return_source_documents=True
            )
            
            logger.info("QA chain initialized with RAG")
            
        except Exception as e:
            logger.error(f"Error initializing QA chain: {str(e)}")
            raise
    
    async def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the vector store"""
        try:
            if not self.vector_store:
                logger.error("Vector store not initialized")
                return False
            
            # Split documents into chunks
            texts = self.text_splitter.split_documents(documents)
            
            # Add to vector store
            if settings.VECTOR_DB_TYPE == "chroma":
                self.vector_store.add_documents(texts)
            elif settings.VECTOR_DB_TYPE == "faiss":
                if self.vector_store is None:
                    self.vector_store = FAISS.from_documents(
                        texts, self.embeddings
                    )
                else:
                    self.vector_store.add_documents(texts)
                
                # Save FAISS index
                self.vector_store.save_local(VECTOR_DB_CONFIG["faiss"]["index_path"])
            
            logger.info(f"Added {len(texts)} document chunks to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False
    
    async def search_documents(
        self, 
        query: str, 
        limit: int = None,
        threshold: float = None
    ) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        try:
            if not self.vector_store:
                logger.warning("No vector store available for search")
                return []
            
            limit = limit or settings.TOP_K_RESULTS
            threshold = threshold or settings.SIMILARITY_THRESHOLD
            
            # Perform similarity search
            docs = self.vector_store.similarity_search_with_score(
                query, k=limit
            )
            
            # Filter by threshold and format results
            results = []
            for doc, score in docs:
                if score <= (1 - threshold):  # Convert similarity to distance
                    results.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "similarity_score": 1 - score,
                        "source": doc.metadata.get("source", "unknown")
                    })
            
            logger.info(f"Found {len(results)} relevant documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    async def generate_response(
        self,
        query: str,
        conversation_id: str = None,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate response using RAG"""
        try:
            response_data = {
                "response": "",
                "sources": [],
                "confidence": 0.0
            }
            
            # Get or create conversation session
            if conversation_id:
                if conversation_id not in self.conversation_sessions:
                    self.conversation_sessions[conversation_id] = ConversationBufferMemory(
                        memory_key="chat_history",
                        return_messages=True
                    )
                session_memory = self.conversation_sessions[conversation_id]
            else:
                session_memory = self.memory
            
            if self.qa_chain:
                # Use RAG for response generation
                result = await asyncio.get_event_loop().run_in_executor(
                    None, self.qa_chain, {"query": query}
                )
                
                response_data["response"] = result["result"]
                
                # Extract sources
                if "source_documents" in result:
                    response_data["sources"] = [
                        {
                            "content": doc.page_content[:500] + "...",
                            "source": doc.metadata.get("source", "unknown"),
                            "relevance": "high"
                        }
                        for doc in result["source_documents"]
                    ]
                
                # Calculate confidence based on source relevance
                response_data["confidence"] = min(0.9, len(response_data["sources"]) * 0.2)
                
            else:
                # Fallback to direct LLM call
                if self.llm:
                    response = await self.llm.agenerate([query])
                    response_data["response"] = response.generations[0][0].text
                    response_data["confidence"] = 0.7
            
            # Update conversation memory
            session_memory.save_context(
                {"input": query},
                {"output": response_data["response"]}
            )
            
            logger.info(f"Generated response for query: {query[:100]}...")
            return response_data
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error while processing your request.",
                "sources": [],
                "confidence": 0.0
            }
    
    async def log_conversation(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str
    ):
        """Log conversation for learning and analysis"""
        try:
            # This would typically save to a database
            conversation_log = {
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow().isoformat(),
                "user_message": user_message,
                "assistant_response": assistant_response,
                "metadata": {}
            }
            
            # Save to conversation history
            # Implementation would depend on your database choice
            logger.info(f"Logged conversation: {conversation_id}")
            
        except Exception as e:
            logger.error(f"Error logging conversation: {str(e)}")
    
    async def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get conversation history"""
        try:
            if conversation_id in self.conversation_sessions:
                memory = self.conversation_sessions[conversation_id]
                return memory.chat_memory.messages[-limit:]
            return []
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    async def clear_conversation(self, conversation_id: str):
        """Clear conversation history"""
        try:
            if conversation_id in self.conversation_sessions:
                del self.conversation_sessions[conversation_id]
            logger.info(f"Cleared conversation: {conversation_id}")
            
        except Exception as e:
            logger.error(f"Error clearing conversation: {str(e)}")

