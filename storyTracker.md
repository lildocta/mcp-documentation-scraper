# MCP Documentation Scraper - Story Tracker

## Project Overview
Building an MCP (Model Context Protocol) server that scrapes documentation from help articles online, indexes them, and caches them locally for efficient retrieval by LLMs.

## MVP Features
The initial version should focus on core functionality with these primary features:

### Epic 1: MCP Server Foundation
**Goal**: Set up the basic MCP server infrastructure

#### Stories:
- [x] **Story 1.1**: Set up MCP server boilerplate
  - **Acceptance Criteria**:
    - MCP server can be started and accepts connections ✅
    - Basic server configuration is in place ✅
    - Health check endpoint available ✅
  - **Priority**: High
  - **Status**: COMPLETED
  - **Notes**: 
    - Implemented MCP-compatible server using FastAPI
    - Includes health check, capabilities, and tool call endpoints
    - Server follows MCP patterns and can be upgraded to full MCP when Python 3.10+ is available
    - Added start_server.py and test_server.py for easy testing

- [x] **Story 1.2**: Define MCP tools/capabilities
  - **Acceptance Criteria**:
    - Define scraping tool interface ✅
    - Define search tool interface ✅
    - Define indexing tool interface ✅
  - **Priority**: High
  - **Status**: COMPLETED
  - **Notes**:
    - Created comprehensive tool interfaces in `src/tools/` directory
    - Implemented `BaseTool` abstract base class for consistency
    - `ScrapingTool` provides URL scraping and content parsing capabilities
    - `SearchTool` provides keyword, semantic, and hybrid search capabilities
    - `IndexingTool` provides document management and index operations
    - All tools follow MCP protocol patterns with proper input/output schemas

### Epic 2: Web Scraping Tool
**Goal**: Build a robust web scraping mechanism for documentation

#### Stories:
- [ ] **Story 2.1**: Basic web scraper implementation
  - **Acceptance Criteria**:
    - Can fetch HTML content from URLs
    - Handles basic error cases (404, timeouts, etc.)
    - Respects robots.txt
    - Rate limiting to avoid overwhelming servers
  - **Priority**: High

- [ ] **Story 2.2**: Content parser for documentation
  - **Acceptance Criteria**:
    - Extracts main content from HTML (removes navigation, ads, etc.)
    - Handles common documentation formats (markdown-like, structured HTML)
    - Preserves important formatting (code blocks, lists, headers)
    - Extracts metadata (title, description, etc.)
  - **Priority**: High

- [ ] **Story 2.3**: URL validation and preprocessing
  - **Acceptance Criteria**:
    - Validates URLs before scraping
    - Handles redirects appropriately
    - Supports common documentation sites (GitHub, GitLab, readthedocs, etc.)
  - **Priority**: Medium

### Epic 3: Local Storage System
**Goal**: Create efficient local storage for scraped documentation

#### Stories:
- [ ] **Story 3.1**: Documentation storage folder structure
  - **Acceptance Criteria**:
    - Organized folder structure for different documentation sources
    - Naming convention for files that avoids conflicts
    - Metadata files alongside content files
  - **Priority**: High

- [ ] **Story 3.2**: File-based caching system
  - **Acceptance Criteria**:
    - Stores scraped content as structured files
    - Implements cache expiration/refresh logic
    - Handles file I/O errors gracefully
    - Prevents duplicate storage of same content
  - **Priority**: High

### Epic 4: Documentation Index
**Goal**: Build searchable index for efficient content retrieval

#### Stories:
- [ ] **Story 4.1**: Basic indexing system
  - **Acceptance Criteria**:
    - Creates searchable index of scraped content
    - Supports keyword-based search
    - Fast retrieval of relevant documents
    - Updates index when new content is added
  - **Priority**: High

- [ ] **Story 4.2**: Semantic search capabilities
  - **Acceptance Criteria**:
    - Implements vector-based search for better relevance
    - Can find documents based on meaning, not just keywords
    - Ranked results by relevance
  - **Priority**: Medium

### Epic 5: LLM Integration Guide
**Goal**: Provide clear instructions for LLM to use the documentation effectively

#### Stories:
- [ ] **Story 5.1**: Create instruction file template
  - **Acceptance Criteria**:
    - Clear instructions for how LLM should query the system
    - Examples of effective search queries
    - Guidelines on when to use cached vs. fresh content
  - **Priority**: High

- [ ] **Story 5.2**: Context optimization for LLMs
  - **Acceptance Criteria**:
    - Formats retrieved content optimally for LLM consumption
    - Includes relevant metadata and source information
    - Limits content size to avoid context window issues
  - **Priority**: Medium

## Technical Considerations

### Recommended Libraries:
- **MCP**: `mcp` package for server implementation
- **Web Scraping**: `requests`, `beautifulsoup4`, `trafilatura` for content extraction
- **Indexing**: `whoosh` or `sqlite-fts` for basic search, `sentence-transformers` for semantic search
- **Caching**: `diskcache` or custom file-based system
- **Configuration**: `pydantic` for settings management
- **Testing**: `pytest`, `responses` for HTTP mocking

### MVP Definition of Done:
- [ ] MCP server can be started and connected to
- [ ] Can scrape documentation from a given URL
- [ ] Stores content locally in organized structure
- [ ] Provides searchable index of scraped content
- [ ] Includes instruction file for LLM usage
- [ ] Basic error handling and logging
- [ ] Unit tests for core functionality

## Future Enhancements (Post-MVP):
- [ ] Database backend for better performance
- [ ] Bulk scraping of documentation sites
- [ ] Auto-discovery of related documentation
- [ ] Content freshness monitoring and auto-refresh
- [ ] Advanced semantic search with embeddings
- [ ] Support for different content types (PDFs, videos, etc.)
- [ ] Web UI for managing scraped content
- [ ] Integration with popular documentation platforms

## Notes:
- Start with a simple file-based approach for storage
- Focus on common documentation formats first
- Prioritize reliability over performance for MVP
- Ensure good error handling from the start
