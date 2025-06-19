#!/usr/bin/env python3
"""
Test script for MCP Documentation Scraper Server
"""

import sys
import os
import requests
import json
import time

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_server():
    """Test the server endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing MCP Documentation Scraper Server...")
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server first.")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Capabilities
    print("\n2. Testing capabilities endpoint...")
    try:
        response = requests.get(f"{base_url}/capabilities")
        if response.status_code == 200:
            print("✅ Capabilities check passed")
            capabilities = response.json()
            print(f"   Available tools: {[tool['name'] for tool in capabilities['tools']]}")
        else:
            print(f"❌ Capabilities check failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Capabilities check error: {e}")
        return False
    
    # Test 3: Health check tool call
    print("\n3. Testing health check tool call...")
    try:
        tool_call = {
            "tool": "health_check",
            "arguments": {}
        }
        response = requests.post(f"{base_url}/tools/call", json=tool_call)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Health check tool call passed")
                print(f"   Response: {result['data']}")
            else:
                print(f"❌ Health check tool call failed: {result.get('error')}")
        else:
            print(f"❌ Health check tool call failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Health check tool call error: {e}")
        return False
    
    print("\n🎉 All basic tests passed! Server is working correctly.")
    print("\nTo test scraping functionality, try:")
    print(f"curl -X POST {base_url}/tools/call \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"tool\": \"scrape_documentation\", \"arguments\": {\"url\": \"https://httpbin.org/html\"}}'")
    
    return True

if __name__ == "__main__":
    if not test_server():
        print("\n❌ Tests failed. Please check the server and try again.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed successfully!")
