# MCP Documentation Scraper

## Overview
The MCP Documentation Scraper is a Model Context Protocol (MCP) compatible server for scraping documentation from web articles, indexing them, and caching them locally for efficient retrieval by LLMs.

## 🎉 Story 1.1 - COMPLETED ✅

The first story "Set up MCP server boilerplate" has been successfully completed with the following features:

### Features Implemented

- **MCP-Compatible Server**: FastAPI-based server following MCP patterns
- **Health Check Endpoint**: `/health` for monitoring server status
- **Capabilities Endpoint**: `/capabilities` lists available tools
- **Tool Call Interface**: `/tools/call` for executing MCP tools
- **Three Core Tools**:
  - `scrape_documentation`: Scrape and cache documentation from URLs
  - `search_documentation`: Search through cached documentation
  - `health_check`: Check server and component health

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python start_server.py
```

The server will start on `http://localhost:8000`

### 3. Test the Server

```bash
python test_server.py
```

### 4. Example Usage

```bash
# Scrape a webpage
curl -X POST http://localhost:8000/tools/call \
  -H 'Content-Type: application/json' \
  -d '{"tool": "scrape_documentation", "arguments": {"url": "https://httpbin.org/html"}}'

# Search cached content
curl -X POST http://localhost:8000/tools/call \
  -H 'Content-Type: application/json' \
  -d '{"tool": "search_documentation", "arguments": {"query": "blacksmith"}}'
```

## Core Features
- **Web Scraping**: Fetch content from specified URLs using the WebScraper class.
- **Content Parsing**: Extract relevant information from raw HTML using the ContentParser class.
- **Document Indexing**: Index and store parsed content in a local database with the DocumentIndexer class.
- **Search Functionality**: Search through indexed documents using the SearchEngine class.
- **Local Caching**: Store documents locally for quick access with the LocalCache class.

## Project Structure
```
mcp-doc-scraper
├── src
│   ├── __init__.py
│   ├── server.py
│   ├── scraper
│   │   ├── __init__.py
│   │   ├── web_scraper.py
│   │   └── content_parser.py
│   ├── indexer
│   │   ├── __init__.py
│   │   ├── document_indexer.py
│   │   └── search_engine.py
│   ├── cache
│   │   ├── __init__.py
│   │   ├── local_cache.py
│   │   └── database.py
│   ├── models
│   │   ├── __init__.py
│   │   └── document.py
│   └── utils
│       ├── __init__.py
│       └── config.py
├── tests
│   ├── __init__.py
│   ├── test_scraper.py
│   ├── test_indexer.py
│   └── test_cache.py
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mcp-doc-scraper.git
   cd mcp-doc-scraper
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To start the server and begin scraping, run:
```
python src/server.py
```

## Testing
To run the tests, use:
```
pytest tests/
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.