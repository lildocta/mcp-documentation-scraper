import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from scraper.web_scraper import WebScraper
from scraper.content_parser import ContentParser
from indexer.document_indexer import DocumentIndexer
from cache.local_cache import LocalCache
from utils.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class ScrapeUrlRequest(BaseModel):
    url: str = Field(..., description="URL to scrape documentation from")
    force_refresh: bool = Field(False, description="Force refresh even if cached")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query for finding relevant documentation")
    max_results: int = Field(10, description="Maximum number of results to return")

class ToolCall(BaseModel):
    tool: str = Field(..., description="Name of the tool to call")
    arguments: Dict[str, Any] = Field(..., description="Arguments for the tool")

class ToolResponse(BaseModel):
    success: bool
    data: Any = None
    error: str = None

class MCPCompatibleServer:
    """
    MCP-compatible documentation scraper server.
    This implementation follows MCP patterns but uses FastAPI for now.
    Can be upgraded to full MCP when Python 3.10+ is available.
    """
    
    def __init__(self):
        self.app = FastAPI(
            title="MCP Documentation Scraper",
            description="A server for scraping documentation from help articles, indexing them, and caching locally",
            version="0.1.0"
        )
        
        # Initialize components
        self.web_scraper = WebScraper()
        self.content_parser = ContentParser()
        self.document_indexer = DocumentIndexer()
        self.local_cache = LocalCache()
        
        # Setup routes
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup FastAPI routes following MCP patterns"""
        
        @self.app.get("/")
        async def root():
            """Root endpoint with server information"""
            return {
                "name": "mcp-documentation-scraper",
                "version": "0.1.0",
                "description": "MCP-compatible documentation scraper server",
                "capabilities": [
                    "scrape_documentation",
                    "search_documentation", 
                    "health_check"
                ]
            }
        
        @self.app.get("/capabilities")
        async def get_capabilities():
            """Get server capabilities (MCP-style)"""
            return {
                "tools": [
                    {
                        "name": "scrape_documentation",
                        "description": "Scrape documentation from a URL and store it locally",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "URL to scrape documentation from"
                                },
                                "force_refresh": {
                                    "type": "boolean",
                                    "description": "Force refresh even if cached",
                                    "default": False
                                }
                            },
                            "required": ["url"]
                        }
                    },
                    {
                        "name": "search_documentation",
                        "description": "Search through cached documentation",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query for finding relevant documentation"
                                },
                                "max_results": {
                                    "type": "integer",
                                    "description": "Maximum number of results to return",
                                    "default": 10
                                }
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "health_check",
                        "description": "Check server health and status",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                ]
            }
        
        @self.app.post("/tools/call")
        async def call_tool(tool_call: ToolCall) -> ToolResponse:
            """Call a tool (MCP-style endpoint)"""
            try:
                if tool_call.tool == "scrape_documentation":
                    result = await self._handle_scrape_documentation(tool_call.arguments)
                elif tool_call.tool == "search_documentation":
                    result = await self._handle_search_documentation(tool_call.arguments)
                elif tool_call.tool == "health_check":
                    result = await self._handle_health_check(tool_call.arguments)
                else:
                    return ToolResponse(success=False, error=f"Unknown tool: {tool_call.tool}")
                
                return ToolResponse(success=True, data=result)
                
            except Exception as e:
                logger.error(f"Error calling tool {tool_call.tool}: {e}")
                return ToolResponse(success=False, error=str(e))
        
        @self.app.get("/health")
        async def health_check():
            """Simple health check endpoint"""
            try:
                result = await self._handle_health_check({})
                return {"status": "healthy", "details": result}
            except Exception as e:
                return {"status": "unhealthy", "error": str(e)}

    async def _handle_scrape_documentation(self, arguments: dict) -> dict:
        """Handle documentation scraping"""
        request = ScrapeUrlRequest(**arguments)
        
        try:
            # Check cache first unless force refresh is requested
            if not request.force_refresh:
                cached_doc = self.local_cache.get_cached_document(request.url)
                if cached_doc:
                    return {
                        "message": f"Retrieved from cache: {cached_doc.get('title', 'Untitled')}",
                        "url": request.url,
                        "source": "cache",
                        "document": cached_doc
                    }
            
            # Scrape the documentation
            raw_html = self.web_scraper.scrape_article(request.url)
            
            # Parse the content
            parsed_data = self.content_parser.parse_content(raw_html, request.url)
            
            # Index the document
            self.document_indexer.index_document(parsed_data)
            
            # Cache the document
            self.local_cache.cache_document(request.url, parsed_data)
            
            return {
                "message": f"Successfully scraped and cached: {parsed_data.get('title', 'Untitled')}",
                "url": request.url,
                "source": "scraped",
                "document": parsed_data
            }
            
        except Exception as e:
            logger.error(f"Error scraping documentation: {e}")
            raise e

    async def _handle_search_documentation(self, arguments: dict) -> dict:
        """Handle documentation search"""
        request = SearchRequest(**arguments)
        
        try:
            # Search through indexed documents
            results = self.document_indexer.search(request.query, max_results=request.max_results)
            
            return {
                "query": request.query,
                "total_results": len(results),
                "max_results": request.max_results,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error searching documentation: {e}")
            raise e

    async def _handle_health_check(self, arguments: dict) -> dict:
        """Handle health check"""
        try:
            # Perform basic health checks
            cache_status = "OK" if self.local_cache.is_healthy() else "ERROR"
            indexer_status = "OK" if self.document_indexer.is_healthy() else "ERROR"
            
            return {
                "server": "OK",
                "cache": cache_status,
                "indexer": indexer_status,
                "configuration": "OK",
                "cache_directory": Config.CACHE_DIR
            }
            
        except Exception as e:
            logger.error(f"Error during health check: {e}")
            raise e

# Global server instance
server_instance = MCPCompatibleServer()
app = server_instance.app

async def main():
    """Run the server"""
    logger.info("Starting MCP Documentation Scraper server...")
    logger.info(f"Cache directory: {Config.CACHE_DIR}")
    
    # Run the server
    config = uvicorn.Config(
        app,
        host="localhost",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())