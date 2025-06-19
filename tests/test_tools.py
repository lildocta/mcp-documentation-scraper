"""
Tests for MCP Tool Interfaces

This module contains tests for the tool interface definitions.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Dict, Any
from datetime import datetime

from src.tools.base_tool import BaseTool, ToolResult, ToolCapability
from src.tools.scraping_tool import ScrapingTool, ScrapingResult
from src.tools.search_tool import SearchTool, SearchResult, SearchResponse
from src.tools.indexing_tool import IndexingTool, Document, IndexStats


class TestBaseTool:
    """Test the BaseTool abstract base class."""
    
    def test_tool_result_creation(self):
        """Test ToolResult creation with different parameters."""
        # Success result
        result = ToolResult(success=True, data={"test": "data"})
        assert result.success is True
        assert result.data == {"test": "data"}
        assert result.error is None
        
        # Error result
        result = ToolResult(success=False, error="Test error")
        assert result.success is False
        assert result.error == "Test error"
        assert result.data is None
    
    def test_tool_capability_creation(self):
        """Test ToolCapability creation."""
        capability = ToolCapability(
            name="test_capability",
            description="Test capability",
            input_schema={"type": "object", "properties": {"param": {"type": "string"}}}
        )
        assert capability.name == "test_capability"
        assert capability.description == "Test capability"
        assert "param" in capability.input_schema["properties"]
    
    def test_validate_parameters_basic(self):
        """Test basic parameter validation."""
        # Create a concrete implementation for testing
        class TestTool(BaseTool):
            @property
            def name(self) -> str:
                return "test_tool"
            
            @property
            def description(self) -> str:
                return "Test tool"
            
            @property
            def capabilities(self):
                return [
                    ToolCapability(
                        name="test_cap",
                        description="Test capability",
                        input_schema={
                            "type": "object",
                            "properties": {"required_param": {"type": "string"}},
                            "required": ["required_param"]
                        }
                    )
                ]
            
            async def execute(self, capability_name: str, parameters: Dict[str, Any]) -> ToolResult:
                return ToolResult(success=True)
        
        tool = TestTool()
        
        # Valid parameters
        assert tool.validate_parameters("test_cap", {"required_param": "value"}) is True
        
        # Missing required parameter
        assert tool.validate_parameters("test_cap", {}) is False
        
        # Unknown capability
        assert tool.validate_parameters("unknown", {"param": "value"}) is False


class TestScrapingTool:
    """Test the ScrapingTool interface."""
    
    def test_tool_properties(self):
        """Test ScrapingTool properties."""
        # Create a concrete implementation for testing
        class TestScrapingTool(ScrapingTool):
            async def scrape_url(self, url: str, **kwargs) -> ScrapingResult:
                return ScrapingResult(url=url, title="Test", content="Test content")
            
            async def scrape_multiple_urls(self, urls, **kwargs):
                return [ScrapingResult(url=url, title="Test") for url in urls]
            
            async def parse_content(self, html: str, url=None, **kwargs) -> ScrapingResult:
                return ScrapingResult(url=url or "unknown", content=html)
        
        tool = TestScrapingTool()
        assert tool.name == "scraping_tool"
        assert "scraping" in tool.description.lower()
        assert len(tool.capabilities) == 3
        
        # Check capability names
        cap_names = [cap.name for cap in tool.capabilities]
        assert "scrape_url" in cap_names
        assert "scrape_multiple_urls" in cap_names
        assert "parse_content" in cap_names
    
    def test_scraping_result_creation(self):
        """Test ScrapingResult creation."""
        result = ScrapingResult(
            url="https://example.com",
            title="Test Page",
            content="Test content",
            status_code=200
        )
        assert result.url == "https://example.com"
        assert result.title == "Test Page"
        assert result.content == "Test content"
        assert result.status_code == 200
        assert result.error is None
    
    @pytest.mark.asyncio
    async def test_execute_method(self):
        """Test the execute method routing."""
        class TestScrapingTool(ScrapingTool):
            async def scrape_url(self, url: str, **kwargs) -> ScrapingResult:
                return ScrapingResult(url=url, title="Test", content="Test content")
            
            async def scrape_multiple_urls(self, urls, **kwargs):
                return [ScrapingResult(url=url, title="Test") for url in urls]
            
            async def parse_content(self, html: str, url=None, **kwargs) -> ScrapingResult:
                return ScrapingResult(url=url or "unknown", content=html)
        
        tool = TestScrapingTool()
        
        # Test scrape_url
        result = await tool.execute("scrape_url", {"url": "https://example.com"})
        assert result.success is True
        assert result.data.url == "https://example.com"
        
        # Test unknown capability
        result = await tool.execute("unknown", {})
        assert result.success is False
        assert "Unknown capability" in result.error


class TestSearchTool:
    """Test the SearchTool interface."""
    
    def test_tool_properties(self):
        """Test SearchTool properties."""
        # Create a concrete implementation for testing
        class TestSearchTool(SearchTool):
            async def search(self, query: str, **kwargs) -> SearchResponse:
                return SearchResponse(
                    query=query,
                    results=[],
                    total_results=0,
                    search_time=0.1
                )
            
            async def suggest(self, partial_query: str, limit: int = 5):
                return [f"{partial_query}_suggestion_{i}" for i in range(limit)]
            
            async def similar(self, document_id: str, limit: int = 5, threshold: float = 0.5):
                return []
        
        tool = TestSearchTool()
        assert tool.name == "search_tool"
        assert "search" in tool.description.lower()
        assert len(tool.capabilities) == 3
        
        # Check capability names
        cap_names = [cap.name for cap in tool.capabilities]
        assert "search" in cap_names
        assert "suggest" in cap_names
        assert "similar" in cap_names
    
    def test_search_result_creation(self):
        """Test SearchResult creation."""
        result = SearchResult(
            document_id="doc1",
            title="Test Document",
            content="Test content",
            score=0.85
        )
        assert result.document_id == "doc1"
        assert result.title == "Test Document"
        assert result.score == 0.85
    
    def test_search_response_creation(self):
        """Test SearchResponse creation."""
        results = [
            SearchResult(document_id="doc1", title="Doc 1", content="Content 1"),
            SearchResult(document_id="doc2", title="Doc 2", content="Content 2")
        ]
        response = SearchResponse(
            query="test query",
            results=results,
            total_results=2,
            search_time=0.15
        )
        assert response.query == "test query"
        assert len(response.results) == 2
        assert response.total_results == 2
        assert response.search_time == 0.15


class TestIndexingTool:
    """Test the IndexingTool interface."""
    
    def test_tool_properties(self):
        """Test IndexingTool properties."""
        # Create a concrete implementation for testing
        class TestIndexingTool(IndexingTool):
            async def add_document(self, document: Document, update_if_exists: bool = False) -> bool:
                return True
            
            async def update_document(self, document_id: str, updates: Dict[str, Any]) -> bool:
                return True
            
            async def remove_document(self, document_id: str) -> bool:
                return True
            
            async def get_document(self, document_id: str, include_content: bool = True):
                return Document(id=document_id, title="Test", content="Content")
            
            async def list_documents(self, **kwargs):
                return []
            
            async def get_index_stats(self) -> IndexStats:
                return IndexStats(total_documents=0, total_size_bytes=0)
            
            async def rebuild_index(self, force: bool = False) -> bool:
                return True
        
        tool = TestIndexingTool()
        assert tool.name == "indexing_tool"
        assert "indexing" in tool.description.lower()
        assert len(tool.capabilities) == 7
        
        # Check capability names
        cap_names = [cap.name for cap in tool.capabilities]
        expected_caps = [
            "add_document", "update_document", "remove_document",
            "get_document", "list_documents", "get_index_stats", "rebuild_index"
        ]
        for cap in expected_caps:
            assert cap in cap_names
    
    def test_document_creation(self):
        """Test Document creation."""
        now = datetime.now()
        doc = Document(
            id="doc1",
            title="Test Document",
            content="Test content",
            url="https://example.com",
            source="test_source",
            tags=["tag1", "tag2"],
            created_at=now
        )
        assert doc.id == "doc1"
        assert doc.title == "Test Document"
        assert doc.content == "Test content"
        assert doc.url == "https://example.com"
        assert doc.source == "test_source"
        assert "tag1" in doc.tags
        assert doc.created_at == now
    
    def test_index_stats_creation(self):
        """Test IndexStats creation."""
        stats = IndexStats(
            total_documents=100,
            total_size_bytes=1024000,
            sources={"source1": 50, "source2": 50}
        )
        assert stats.total_documents == 100
        assert stats.total_size_bytes == 1024000
        assert stats.sources["source1"] == 50
    
    @pytest.mark.asyncio
    async def test_execute_method(self):
        """Test the execute method with document operations."""
        class TestIndexingTool(IndexingTool):
            async def add_document(self, document: Document, update_if_exists: bool = False) -> bool:
                return True
            
            async def update_document(self, document_id: str, updates: Dict[str, Any]) -> bool:
                return True
            
            async def remove_document(self, document_id: str) -> bool:
                return True
            
            async def get_document(self, document_id: str, include_content: bool = True):
                return Document(id=document_id, title="Test", content="Content")
            
            async def list_documents(self, **kwargs):
                return []
            
            async def get_index_stats(self) -> IndexStats:
                return IndexStats(total_documents=0, total_size_bytes=0)
            
            async def rebuild_index(self, force: bool = False) -> bool:
                return True
        
        tool = TestIndexingTool()
        
        # Test add_document
        result = await tool.execute("add_document", {
            "document": {
                "id": "test_doc",
                "title": "Test",
                "content": "Content"
            }
        })
        assert result.success is True
        assert result.data["added"] is True
        
        # Test get_index_stats
        result = await tool.execute("get_index_stats", {})
        assert result.success is True
        assert isinstance(result.data, IndexStats)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
