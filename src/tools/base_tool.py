"""
Base Tool Interface

This module defines the abstract base class for all MCP tools.
All tools should inherit from this base class to ensure consistency.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ToolResult:
    """Standard result format for all tool operations."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass 
class ToolCapability:
    """Describes a tool's capability for MCP protocol."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Optional[Dict[str, Any]] = None


class BaseTool(ABC):
    """
    Abstract base class for all MCP tools.
    
    This class defines the common interface that all tools must implement
    to be compatible with the MCP server.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this tool."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what this tool does."""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> List[ToolCapability]:
        """Return a list of capabilities this tool provides."""
        pass
    
    @abstractmethod
    async def execute(self, capability_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """
        Execute a specific capability of this tool.
        
        Args:
            capability_name: The name of the capability to execute
            parameters: Parameters for the capability execution
            
        Returns:
            ToolResult containing the execution result
        """
        pass
    
    def validate_parameters(self, capability_name: str, parameters: Dict[str, Any]) -> bool:
        """
        Validate parameters for a specific capability.
        
        Args:
            capability_name: The name of the capability
            parameters: Parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        # Default implementation - subclasses can override for custom validation
        capability = next((cap for cap in self.capabilities if cap.name == capability_name), None)
        if not capability:
            return False
        
        # Basic validation - check required parameters exist
        required_params = capability.input_schema.get("required", [])
        return all(param in parameters for param in required_params)
