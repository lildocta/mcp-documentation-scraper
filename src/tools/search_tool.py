"""
Search Tool Interface

This module defines the interface for searching through indexed documentation.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from .base_tool import BaseTool, ToolResult, ToolCapability


@dataclass
class SearchResult:
    """A single search result."""
    document_id: str
    title: str
    content: str
    url: Optional[str] = None
    score: float = 0.0
    snippet: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SearchResponse:
    """Response from a search operation."""
    query: str
    results: List[SearchResult]
    total_results: int
    search_time: float
    metadata: Optional[Dict[str, Any]] = None


class SearchTool(BaseTool):
    """
    Interface for search functionality.
    
    This tool provides capabilities for searching through indexed documentation
    using various search methods (keyword, semantic, hybrid).
    """
    
    @property
    def name(self) -> str:
        return "search_tool"
    
    @property
    def description(self) -> str:
        return "Tool for searching indexed documentation content"
    
    @property
    def capabilities(self) -> List[ToolCapability]:
        return [
            ToolCapability(
                name="search",
                description="Search for documents matching a query",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "search_type": {
                            "type": "string",
                            "enum": ["keyword", "semantic", "hybrid"],
                            "description": "Type of search to perform",
                            "default": "hybrid"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Maximum number of results to return",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        },
                        "filters": {
                            "type": "object",
                            "description": "Additional filters to apply",
                            "properties": {
                                "source": {"type": "string"},
                                "tags": {"type": "array", "items": {"type": "string"}},
                                "date_range": {
                                    "type": "object",
                                    "properties": {
                                        "start": {"type": "string", "format": "date"},
                                        "end": {"type": "string", "format": "date"}
                                    }
                                }
                            }
                        },
                        "include_snippets": {
                            "type": "boolean",
                            "description": "Whether to include content snippets",
                            "default": True
                        }
                    },
                    "required": ["query"]
                }
            ),
            ToolCapability(
                name="suggest",
                description="Get search suggestions based on partial query",
                input_schema={
                    "type": "object",
                    "properties": {
                        "partial_query": {
                            "type": "string",
                            "description": "Partial search query for suggestions"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Maximum number of suggestions",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 20
                        }
                    },
                    "required": ["partial_query"]
                }
            ),
            ToolCapability(
                name="similar",
                description="Find documents similar to a given document",
                input_schema={
                    "type": "object",
                    "properties": {
                        "document_id": {
                            "type": "string",
                            "description": "ID of the document to find similar documents for"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Maximum number of similar documents",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 50
                        },
                        "threshold": {
                            "type": "number",
                            "description": "Similarity threshold (0-1)",
                            "default": 0.5,
                            "minimum": 0,
                            "maximum": 1
                        }
                    },
                    "required": ["document_id"]
                }
            )
        ]
    
    async def search(
        self, 
        query: str, 
        search_type: str = "hybrid",
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        include_snippets: bool = True
    ) -> SearchResponse:
        """
        Search for documents matching a query.
        
        Args:
            query: The search query
            search_type: Type of search ("keyword", "semantic", "hybrid")
            limit: Maximum number of results
            filters: Additional filters to apply
            include_snippets: Whether to include content snippets
            
        Returns:
            SearchResponse with matching documents
        """
        raise NotImplementedError("Subclasses must implement search")
    
    async def suggest(self, partial_query: str, limit: int = 5) -> List[str]:
        """
        Get search suggestions based on partial query.
        
        Args:
            partial_query: Partial search query
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested queries
        """
        raise NotImplementedError("Subclasses must implement suggest")
    
    async def similar(
        self, 
        document_id: str, 
        limit: int = 5, 
        threshold: float = 0.5
    ) -> List[SearchResult]:
        """
        Find documents similar to a given document.
        
        Args:
            document_id: ID of the reference document
            limit: Maximum number of similar documents
            threshold: Similarity threshold
            
        Returns:
            List of similar documents
        """
        raise NotImplementedError("Subclasses must implement similar")
    
    async def execute(self, capability_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """Execute a search capability."""
        try:
            if capability_name == "search":
                result = await self.search(**parameters)
                return ToolResult(success=True, data=result)
            
            elif capability_name == "suggest":
                result = await self.suggest(**parameters)
                return ToolResult(success=True, data=result)
            
            elif capability_name == "similar":
                result = await self.similar(**parameters)
                return ToolResult(success=True, data=result)
            
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
