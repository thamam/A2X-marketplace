# Research Findings: Claude Memory Plugin

**Session:** memory-management-plugin
**Date:** 2025-12-30

---

## Research Summary

### MCP Server Patterns

**Source:** https://github.com/modelcontextprotocol/typescript-sdk

**Key Findings:**
- Official MCP TypeScript SDK package: `@modelcontextprotocol/sdk`
- Server class: `Server` from `@modelcontextprotocol/sdk/server/index.js`
- Transport: `StdioServerTransport` for standard input/output communication
- Tool registration: `setRequestHandler(CallToolRequestSchema, handler)`
- Schema validation: Use Zod for type-safe tool arguments

**Pattern Used:**
```typescript
const server = new Server(
  { name: 'claude-memory', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Handle tool calls
});
```

---

### Memory Management Patterns

**Source:** https://github.com/basicmachines-co/basic-memory (2,291 stars)

**Key Findings:**
- **Local-first architecture** - Store everything locally for privacy
- **Hybrid storage** - Structured (SQLite) + Unstructured (Markdown)
- **Semantic search** - ChromaDB for vector embeddings
- **Markdown format** - Human-readable memory files
- **Auto-indexing** - Background indexing for search performance

**Architecture Adopted:**
- `.claude-memory/` directory structure
- SQLite for metadata and full-text search
- Markdown files for conversations and knowledge
- JSON for sessions
- Vector embeddings in SQLite BLOB columns

---

### Vector Search Implementation

**Source:** https://github.com/lancedb/lancedb

**Key Findings:**
- LanceDB is available but heavyweight
- Simpler approach: Store embeddings in SQLite
- Use `@xenova/transformers` for local embedding generation
- Cosine similarity for vector search

**Decision:**
- Use `@xenova/transformers` (Transformers.js) - runs locally in Node.js
- Store embeddings as Float32Array in SQLite BLOB
- Implement cosine similarity search in TypeScript
- No external vector database needed

---

### Embedding Models

**Source:** https://huggingface.co/models

**Models Selected:**

| Model | HuggingFace ID | Size | Dimensions | Use Case |
|-------|----------------|------|------------|----------|
| MiniLM-L6 | `Xenova/all-MiniLM-L6-v2` | 80MB | 384 | Default - fast and good quality |
| MiniLM-L12 | `Xenova/all-MiniLM-L12-v2` | 120MB | 384 | Better quality, slower |
| MPNet-Base | `Xenova/all-mpnet-base-v2` | 420MB | 768 | Best quality, slowest |

**Implementation:**
- Configurable via `EMBEDDING_MODEL` environment variable
- Lazy loading - model downloads on first use
- Batch processing for multiple texts
- Automatic text truncation to max tokens

---

## Architecture Decisions

### 1. Storage Layer

**Decision:** Hybrid SQLite + Markdown

**Rationale:**
- SQLite: Fast metadata queries, full-text search (FTS5), vector storage
- Markdown: Human-readable, easily exportable, version-control friendly
- Best of both worlds: Performance + Transparency

**Implementation:**
- `storage/database.ts` - SQLite operations
- `storage/filesystem.ts` - File operations
- `storage/index.ts` - Unified interface

---

### 2. Search Strategy

**Decision:** Dual search - Keyword (FTS) + Semantic (Vectors)

**Rationale:**
- Keyword search: Fast, exact matches, good for known terms
- Semantic search: Understands context, finds related concepts
- User chooses based on needs

**Implementation:**
- FTS5 virtual table for keyword search
- Vector embeddings + cosine similarity for semantic search
- `recall` tool supports both via `useSemanticSearch` flag

---

### 3. Local-First Embeddings

**Decision:** Use `@xenova/transformers` instead of OpenAI API

**Rationale:**
- **Privacy:** No data sent to external services
- **Cost:** No API fees
- **Offline:** Works without internet
- **Speed:** No network latency (after initial download)

**Trade-offs:**
- Initial model download (80-420MB)
- Slightly lower quality than GPT embeddings
- Higher initial latency (model loading)

**Accepted because:** Privacy and cost savings outweigh quality difference

---

### 4. TypeScript Over Python

**Decision:** Build MCP server in TypeScript, not Python

**Rationale:**
- Better integration with Claude Code (Node.js-based)
- Transformers.js provides local embeddings in JavaScript
- Single runtime environment
- Easier for users to install (npm vs pip + Python env)

**Trade-offs:**
- Python has richer ML ecosystem
- Transformers.js is newer, less mature

**Accepted because:** Installation simplicity and Claude Code compatibility

---

### 5. Configurable Models

**Decision:** Let users choose embedding model

**Rationale:**
- Different users have different needs (speed vs quality)
- Disk space constraints vary
- Power users want best quality, casual users want fast

**Implementation:**
- `EMBEDDING_MODEL` environment variable
- Model configs in `embeddings/models.ts`
- Auto-fallback to default if invalid model specified

---

## Implementation Highlights

### Storage Layer (2,500+ lines)

**Files:**
- `storage/types.ts` - TypeScript interfaces
- `storage/database.ts` - SQLite with FTS5
- `storage/filesystem.ts` - Markdown/JSON file operations
- `storage/index.ts` - Unified storage manager

**Features:**
- CRUD operations for memories, conversations, knowledge, sessions
- Full-text search with FTS5
- Vector embedding storage
- Auto-archival based on age
- Storage size limits
- Statistics and cleanup operations

---

### Embeddings Layer (500+ lines)

**Files:**
- `embeddings/models.ts` - Model configurations
- `embeddings/generator.ts` - Embedding generation
- `embeddings/search.ts` - Semantic search

**Features:**
- Lazy model initialization
- Batch embedding generation
- Cosine similarity search
- Configurable models (3 options)
- Progress logging

---

### MCP Server (800+ lines)

**Files:**
- `tools/memory-tools.ts` - Tool implementations
- `server.ts` - MCP server setup
- `index.ts` - Entry point

**Tools Implemented:**
1. `remember` - Store memory
2. `recall` - Search memories
3. `list_memories` - List all memories
4. `save_conversation` - Save conversation
5. `load_conversation` - Load conversation
6. `save_session` - Save session state
7. `restore_session` - Restore session
8. `search_knowledge` - Semantic knowledge search
9. `get_stats` - Storage statistics

---

### Plugin Components

**Commands:**
- `/remember` - Quick memory storage
- `/recall` - Memory search
- `/list-memories` - Browse memories
- `/save-conversation` - Save chat
- `/load-conversation` - Load chat
- `/save-session` - Save state
- `/restore-session` - Restore state
- `/search-knowledge` - Semantic search

**Skills:**
- `auto-remember` - Automatic memory capture
- `context-aware` - Use memories in responses
- `session-persistence` - Auto save/restore

**Agents:**
- `memory-indexer` - Background indexing
- `knowledge-extractor` - Extract structured knowledge
- `semantic-search` - Advanced search

---

## References

### Official Documentation
- MCP TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- Transformers.js: https://github.com/xenova/transformers.js
- Better-sqlite3: https://github.com/WiseLibs/better-sqlite3

### Inspiration Projects
- basic-memory: https://github.com/basicmachines-co/basic-memory
  - 2,291 stars
  - Local-first memory management
  - ChromaDB for vectors
  - Obsidian integration

- mcp-memory: https://github.com/Puliczek/mcp-memory
  - 105 stars
  - Cloudflare D1 + Vectorize
  - Simpler implementation

### Technical Resources
- MCP Protocol Spec: https://modelcontextprotocol.io
- SQLite FTS5: https://www.sqlite.org/fts5.html
- Sentence Transformers: https://www.sbert.net/
- HuggingFace Models: https://huggingface.co/models

---

## Next Steps (If Continuing)

### Phase 1: Validation
- [ ] Install dependencies (`npm install`)
- [ ] Build TypeScript (`npm run build`)
- [ ] Test MCP server startup
- [ ] Verify tool registration
- [ ] Test each tool manually

### Phase 2: Testing
- [ ] Test memory CRUD operations
- [ ] Test keyword search
- [ ] Test semantic search
- [ ] Test conversation save/load
- [ ] Test session persistence
- [ ] Test archival operations

### Phase 3: Integration
- [ ] Install plugin in Claude Code
- [ ] Test slash commands
- [ ] Verify MCP server connection
- [ ] Test end-to-end workflows
- [ ] Performance testing with large datasets

### Phase 4: Polish
- [ ] Add remaining skills
- [ ] Add remaining agents
- [ ] Add hooks (if supported)
- [ ] Error handling improvements
- [ ] Add logging and debugging
- [ ] Performance optimization

---

**Status:** Core implementation complete, ready for installation and testing

🔍🐙 Created by Octocode MCP - visit https://octocode.ai for more info
