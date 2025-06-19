"""
Scraping Tool Interface

This module defines the interface for the web scraping tool that fetches
and processes documentation from web pages.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from .base_tool import BaseTool, ToolResult, ToolCapability


@dataclass
class ScrapingResult:
    """Result of a scraping operation."""
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None


class ScrapingTool(BaseTool):
    """
    Interface for web scraping functionality.
    
    This tool provides capabilities for fetching web pages, extracting content,
    and parsing documentation from various sources.
    """
    
    @property
    def name(self) -> str:
        return "scraping_tool"
    
    @property
    def description(self) -> str:
        return "Tool for scraping and parsing documentation from web pages"
    
    @property
    def capabilities(self) -> List[ToolCapability]:
        return [
            ToolCapability(
                name="scrape_url",
                description="Scrape content from a single URL",
                input_schema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to scrape"
                        },
                        "include_metadata": {
                            "type": "boolean",
                            "description": "Whether to extract metadata",
                            "default": True
                        },
                        "follow_redirects": {
                            "type": "boolean", 
                            "description": "Whether to follow HTTP redirects",
                            "default": True
                        },
                        "timeout": {
                            "type": "number",
                            "description": "Request timeout in seconds",
                            "default": 30
                        }
                    },
                    "required": ["url"]
                }
            ),
            ToolCapability(
                name="scrape_multiple_urls",
                description="Scrape content from multiple URLs",
                input_schema={
                    "type": "object",
                    "properties": {
                        "urls": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of URLs to scrape"
                        },
                        "include_metadata": {
                            "type": "boolean",
                            "description": "Whether to extract metadata",
                            "default": True
                        },
                        "max_concurrent": {
                            "type": "number",
                            "description": "Maximum concurrent requests",
                            "default": 5
                        },
                        "timeout": {
                            "type": "number",
                            "description": "Request timeout in seconds",
                            "default": 30
                        }
                    },
                    "required": ["urls"]
                }
            ),
            ToolCapability(
                name="parse_content",
                description="Parse and clean HTML content",
                input_schema={
                    "type": "object", 
                    "properties": {
                        "html": {
                            "type": "string",
                            "description": "Raw HTML content to parse"
                        },
                        "url": {
                            "type": "string",
                            "description": "Original URL (for context)"
                        },
                        "extract_code_blocks": {
                            "type": "boolean",
                            "description": "Whether to preserve code block formatting",
                            "default": True
                        },
                        "extract_links": {
                            "type": "boolean",
                            "description": "Whether to extract and resolve links",
                            "default": False
                        }
                    },
                    "required": ["html"]
                }
            )
        ]
    
    async def scrape_url(self, url: str, **kwargs) -> ScrapingResult:
        """
        Scrape content from a single URL.
        
        Args:
            url: The URL to scrape
            **kwargs: Additional scraping options
            
        Returns:
            ScrapingResult with the scraped content
        """
        raise NotImplementedError("Subclasses must implement scrape_url")
    
    async def scrape_multiple_urls(self, urls: List[str], **kwargs) -> List[ScrapingResult]:
        """
        Scrape content from multiple URLs.
        
        Args:
            urls: List of URLs to scrape
            **kwargs: Additional scraping options
            
        Returns:
            List of ScrapingResult objects
        """
        raise NotImplementedError("Subclasses must implement scrape_multiple_urls")
    
    async def parse_content(self, html: str, url: Optional[str] = None, **kwargs) -> ScrapingResult:
        """
        Parse and clean HTML content.
        
        Args:
            html: Raw HTML content
            url: Original URL for context
            **kwargs: Additional parsing options
            
        Returns:
            ScrapingResult with parsed content
        """
        raise NotImplementedError("Subclasses must implement parse_content")
    
    async def execute(self, capability_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """Execute a scraping capability."""
        try:
            if capability_name == "scrape_url":
                result = await self.scrape_url(**parameters)
                return ToolResult(success=True, data=result)
            
            elif capability_name == "scrape_multiple_urls":
                result = await self.scrape_multiple_urls(**parameters)
                return ToolResult(success=True, data=result)
            
            elif capability_name == "parse_content":
                result = await self.parse_content(**parameters)
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
