"""
Indexing Tool Interface

This module defines the interface for indexing and managing documentation.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from .base_tool import BaseTool, ToolResult, ToolCapability


@dataclass
class Document:
    """Represents a document to be indexed."""
    id: str
    title: str
    content: str
    url: Optional[str] = None
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class IndexStats:
    """Statistics about the document index."""
    total_documents: int
    total_size_bytes: int
    last_updated: Optional[datetime] = None
    sources: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None


class IndexingTool(BaseTool):
    """
    Interface for document indexing functionality.
    
    This tool provides capabilities for adding, updating, removing, and managing
    documents in the search index.
    """
    
    @property
    def name(self) -> str:
        return "indexing_tool"
    
    @property
    def description(self) -> str:
        return "Tool for indexing and managing documentation content"
    
    @property
    def capabilities(self) -> List[ToolCapability]:
        return [
            ToolCapability(
                name="add_document",
                description="Add a new document to the index",
                input_schema={
                    "type": "object",
                    "properties": {
                        "document": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "title": {"type": "string"},
                                "content": {"type": "string"},
                                "url": {"type": "string"},
                                "source": {"type": "string"},
                                "tags": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "metadata": {"type": "object"}
                            },
                            "required": ["id", "title", "content"]
                        },
                        "update_if_exists": {
                            "type": "boolean",
                            "description": "Whether to update if document already exists",
                            "default": False
                        }
                    },
                    "required": ["document"]
                }
            ),
            ToolCapability(
                name="update_document",
                description="Update an existing document in the index",
                input_schema={
                    "type": "object",
                    "properties": {
                        "document_id": {
                            "type": "string",
                            "description": "ID of the document to update"
                        },
                        "updates": {
                            "type": "object",
                            "description": "Fields to update",
                            "properties": {
                                "title": {"type": "string"},
                                "content": {"type": "string"},
                                "url": {"type": "string"},
                                "source": {"type": "string"},
                                "tags": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "metadata": {"type": "object"}
                            }
                        }
                    },
                    "required": ["document_id", "updates"]
                }
            ),
            ToolCapability(
                name="remove_document",
                description="Remove a document from the index",
                input_schema={
                    "type": "object",
                    "properties": {
                        "document_id": {
                            "type": "string",
                            "description": "ID of the document to remove"
                        }
                    },
                    "required": ["document_id"]
                }
            ),
            ToolCapability(
                name="get_document",
                description="Retrieve a document by ID",
                input_schema={
                    "type": "object",
                    "properties": {
                        "document_id": {
                            "type": "string",
                            "description": "ID of the document to retrieve"
                        },
                        "include_content": {
                            "type": "boolean",
                            "description": "Whether to include full content",
                            "default": True
                        }
                    },
                    "required": ["document_id"]
                }
            ),
            ToolCapability(
                name="list_documents",
                description="List documents with optional filtering",
                input_schema={
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "Filter by source"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter by tags"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Maximum number of documents",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 1000
                        },
                        "offset": {
                            "type": "number",
                            "description": "Number of documents to skip",
                            "default": 0,
                            "minimum": 0
                        },
                        "include_content": {
                            "type": "boolean",
                            "description": "Whether to include full content",
                            "default": False
                        }
                    }
                }
            ),
            ToolCapability(
                name="get_index_stats",
                description="Get statistics about the document index",
                input_schema={
                    "type": "object",
                    "properties": {}
                }
            ),
            ToolCapability(
                name="rebuild_index",
                description="Rebuild the search index",
                input_schema={
                    "type": "object",
                    "properties": {
                        "force": {
                            "type": "boolean",
                            "description": "Force rebuild even if index is up to date",
                            "default": False
                        }
                    }
                }
            )
        ]
    
    async def add_document(self, document: Document, update_if_exists: bool = False) -> bool:
        """
        Add a new document to the index.
        
        Args:
            document: The document to add
            update_if_exists: Whether to update if document already exists
            
        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement add_document")
    
    async def update_document(self, document_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing document in the index.
        
        Args:
            document_id: ID of the document to update
            updates: Fields to update
            
        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement update_document")
    
    async def remove_document(self, document_id: str) -> bool:
        """
        Remove a document from the index.
        
        Args:
            document_id: ID of the document to remove
            
        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement remove_document")
    
    async def get_document(self, document_id: str, include_content: bool = True) -> Optional[Document]:
        """
        Retrieve a document by ID.
        
        Args:
            document_id: ID of the document to retrieve
            include_content: Whether to include full content
            
        Returns:
            The document if found, None otherwise
        """
        raise NotImplementedError("Subclasses must implement get_document")
    
    async def list_documents(
        self,
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0,
        include_content: bool = False
    ) -> List[Document]:
        """
        List documents with optional filtering.
        
        Args:
            source: Filter by source
            tags: Filter by tags
            limit: Maximum number of documents
            offset: Number of documents to skip
            include_content: Whether to include full content
            
        Returns:
            List of documents
        """
        raise NotImplementedError("Subclasses must implement list_documents")
    
    async def get_index_stats(self) -> IndexStats:
        """
        Get statistics about the document index.
        
        Returns:
            IndexStats with current index information
        """
        raise NotImplementedError("Subclasses must implement get_index_stats")
    
    async def rebuild_index(self, force: bool = False) -> bool:
        """
        Rebuild the search index.
        
        Args:
            force: Force rebuild even if index is up to date
            
        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement rebuild_index")
    
    async def execute(self, capability_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """Execute an indexing capability."""
        try:
            if capability_name == "add_document":
                # Convert dict to Document object
                doc_data = parameters["document"]
                document = Document(**doc_data)
                result = await self.add_document(
                    document, 
                    parameters.get("update_if_exists", False)
                )
                return ToolResult(success=True, data={"added": result})
            
            elif capability_name == "update_document":
                result = await self.update_document(
                    parameters["document_id"],
                    parameters["updates"]
                )
                return ToolResult(success=True, data={"updated": result})
            
            elif capability_name == "remove_document":
                result = await self.remove_document(parameters["document_id"])
                return ToolResult(success=True, data={"removed": result})
            
            elif capability_name == "get_document":
                result = await self.get_document(**parameters)
                return ToolResult(success=True, data=result)
            
            elif capability_name == "list_documents":
                result = await self.list_documents(**parameters)
                return ToolResult(success=True, data=result)
            
            elif capability_name == "get_index_stats":
                result = await self.get_index_stats()
                return ToolResult(success=True, data=result)
            
            elif capability_name == "rebuild_index":
                result = await self.rebuild_index(parameters.get("force", False))
                return ToolResult(success=True, data={"rebuilt": result})
            
            else:
                return ToolResult(
                    success=False,
                    error=f"Unknown capability: {capability_name}"
                )
                
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing {capability_name}: {str(e)}"
            )
