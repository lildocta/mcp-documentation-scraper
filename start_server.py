#!/usr/bin/env python3
"""
Start script for MCP Documentation Scraper Server
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server import main

if __name__ == "__main__":
    import asyncio
    print("Starting MCP Documentation Scraper Server...")
    print("Server will be available at: http://localhost:8000")
    print("Health check endpoint: http://localhost:8000/health")
    print("Capabilities endpoint: http://localhost:8000/capabilities")
    print("Press Ctrl+C to stop the server")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
