# Generation Plan: Claude Code Memory Management Plugin

**Session:** memory-management-plugin
**Date:** 2025-12-30
**Plugin Name:** `claude-memory`

---

## Requirements Summary

**App Type:** Claude Code Plugin with custom MCP server
**Framework:** TypeScript + Python (MCP server)
**Key Features:**
- 💾 Conversation history storage and retrieval
- 📚 Knowledge base building from interactions
- 🔄 Context persistence (save/restore sessions)
- 🔍 Semantic search over memories using vector embeddings

**Target Audience:** Claude Code users who want persistent memory across sessions

---

## Architecture Overview

### Storage Strategy
```
.claude-memory/
├── conversations/          # Conversation transcripts (markdown)
│   ├── 2025-12-30-conversation-1.md
│   └── index.json         # Metadata index
├── knowledge/             # Extracted knowledge entries (markdown)
│   ├── programming-patterns.md
│   ├── user-preferences.md
│   └── index.json
├── sessions/              # Session state snapshots
│   ├── session-2025-12-30-1.json
│   └── index.json
├── vectors/               # Vector embeddings for semantic search
│   └── embeddings.db      # SQLite with vectors
└── memory.db              # Main SQLite database (metadata, search index)
```

### Component Architecture
1. **MCP Server** (`memory-server/`) - Custom MCP server for memory operations
2. **Plugin Components** (`plugins/claude-memory/`)
   - Slash commands: Quick memory operations
   - Skills: Automated memory capture
   - Agents: Background indexing and search
   - Hooks: Conversation lifecycle integration
3. **Storage Layer** - Local files + SQLite + vector embeddings

---

## Research Tasks

### ✅ Completed Research
1. [x] Research: MCP server implementation patterns
   - **Finding:** Use `@modelcontextprotocol/server` with Express/Hono transport
   - **Reference:** https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/src/simpleTaskInteractive.ts

2. [x] Research: Memory management in AI systems
   - **Finding:** basic-memory uses local-first markdown + ChromaDB
   - **Reference:** https://github.com/basicmachines-co/basic-memory

3. [x] Research: Vector search implementations
   - **Finding:** LanceDB for local vector DB, or ChromaDB with Python
   - **Decision:** Use simple embedding storage in SQLite (better.sqlite3 with vector extension)

### Pending Research
- [ ] Research: Claude Code hooks system (how to register lifecycle hooks)
- [ ] Research: Best practices for embedding generation (local vs API)

---

## Technology Stack

### MCP Server
- **Language:** TypeScript
- **Framework:** `@modelcontextprotocol/server` v1.25.1
- **Transport:** Express (HTTP + SSE)
- **Dependencies:**
  - `@modelcontextprotocol/server`
  - `express`
  - `better-sqlite3` - SQLite with extensions
  - `vectordb` or custom vector implementation
  - `@xenova/transformers` - Local embeddings (sentence-transformers)

### Plugin Components
- **Language:** Markdown (commands, skills, agents)
- **Pattern:** Follow maya-toolkit structure

---

## Scaffold Steps

### Phase 1: Project Initialization
1. [ ] Create plugin directory structure
   ```
   plugins/claude-memory/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── README.md
   ├── commands/
   ├── skills/
   ├── agents/
   └── hooks/
   ```

2. [ ] Create MCP server directory structure
   ```
   plugins/claude-memory/mcp-server/
   ├── package.json
   ├── tsconfig.json
   ├── src/
   │   ├── index.ts          # Server entry point
   │   ├── server.ts         # MCP server implementation
   │   ├── storage/          # Storage layer
   │   ├── embeddings/       # Vector embeddings
   │   └── tools/            # MCP tool implementations
   └── dist/                 # Build output
   ```

### Phase 2: MCP Server Implementation
3. [ ] Initialize TypeScript project
   - Create `package.json` with dependencies
   - Configure `tsconfig.json` for Node.js + ESM
   - Add build scripts

4. [ ] Implement storage layer
   - `storage/database.ts` - SQLite setup with better-sqlite3
   - `storage/conversations.ts` - Conversation CRUD operations
   - `storage/knowledge.ts` - Knowledge base operations
   - `storage/sessions.ts` - Session state management

5. [ ] Implement embeddings layer
   - `embeddings/generator.ts` - Generate embeddings using @xenova/transformers
   - `embeddings/search.ts` - Vector similarity search
   - `embeddings/index.ts` - Automatic indexing

6. [ ] Implement MCP server
   - `server.ts` - Define MCP server with tools:
     - `remember` - Store a memory/knowledge entry
     - `recall` - Retrieve memories by query (semantic search)
     - `list_memories` - List all memories with filters
     - `save_conversation` - Save current conversation
     - `load_conversation` - Load past conversation
     - `save_session` - Save session state
     - `restore_session` - Restore session state
     - `search_knowledge` - Semantic search over knowledge base
   - `index.ts` - Server entry point with Express transport

7. [ ] Add CLI commands
   - `src/cli.ts` - Start server, manage memory database

### Phase 3: Plugin Components
8. [ ] Create slash commands
   - `/remember` - Quick memory storage
   - `/recall` - Search memories
   - `/list-memories` - List all memories
   - `/save-conversation` - Save current chat
   - `/load-conversation` - Load previous chat
   - `/save-session` - Save session state
   - `/restore-session` - Restore session
   - `/search-knowledge` - Semantic search

9. [ ] Create skills
   - `auto-remember.md` - Automatically capture important information
   - `context-aware.md` - Use memory to enhance responses
   - `session-persistence.md` - Auto-save session state

10. [ ] Create agents
    - `memory-indexer.md` - Background indexing of conversations
    - `knowledge-extractor.md` - Extract knowledge from conversations
    - `semantic-search.md` - Advanced memory search

11. [ ] Create hooks (if supported)
    - `on-conversation-start.md` - Load relevant memories
    - `on-conversation-end.md` - Save conversation
    - `on-message.md` - Auto-capture important info

### Phase 4: Documentation & Configuration
12. [ ] Create plugin manifest
    - `.claude-plugin/plugin.json` - Plugin metadata

13. [ ] Write README
    - Installation instructions
    - Usage examples
    - MCP server setup
    - Configuration options

14. [ ] Create examples
    - Example memory queries
    - Example knowledge entries
    - Example session workflows

15. [ ] Add configuration files
    - `.env.example` - Environment variables
    - `memory-config.json.example` - Memory settings

---

## Validation Checklist

### MCP Server Validation
- [ ] `npm run build` - TypeScript compiles without errors
- [ ] `npm run dev` - Server starts successfully
- [ ] Server responds to MCP initialize request
- [ ] All tools are registered and callable
- [ ] Storage layer creates/reads/updates files correctly
- [ ] Embeddings generate successfully
- [ ] Semantic search returns relevant results

### Plugin Validation
- [ ] Plugin installs via `/plugin install claude-memory@A2X`
- [ ] All slash commands appear in autocomplete
- [ ] Commands execute without errors
- [ ] Skills activate correctly
- [ ] Agents can be invoked

### Integration Validation
- [ ] Plugin connects to MCP server
- [ ] Memory operations work end-to-end
- [ ] Conversations are saved and loaded correctly
- [ ] Sessions persist and restore
- [ ] Semantic search finds relevant memories
- [ ] No TypeScript `any` escapes (except justified)

---

## Key Decisions & Trade-offs

### ✅ Decisions Made
1. **Local-first architecture** - No external services required
   - Trade-off: Semantic search quality vs simplicity
   - Rationale: Privacy, offline capability, no API costs

2. **Hybrid storage** - SQLite + Markdown files
   - Trade-off: Complexity vs flexibility
   - Rationale: SQLite for queries, markdown for human readability

3. **TypeScript MCP server** - Not Python
   - Trade-off: Embedding quality vs installation complexity
   - Rationale: Better integration with Claude Code (Node.js based)

4. **Local embeddings** - @xenova/transformers
   - Trade-off: Quality vs no API dependencies
   - Rationale: Works offline, no OpenAI API costs

### ⚠️ Open Questions
1. **Hook system** - Does Claude Code support lifecycle hooks?
   - Impact: If no hooks, use skills with manual triggers

2. **Embedding model** - Which sentence-transformer model?
   - Options: all-MiniLM-L6-v2 (fast, small) vs larger models
   - Decision pending: Start with MiniLM, make configurable

3. **Storage limits** - Max conversation/memory size?
   - Impact: Need cleanup/archival strategy
   - Decision pending: Add optional TTL and size limits

---

## Implementation Notes

### Patterns to Follow
- Follow maya-toolkit plugin structure
- Use same documentation style
- Follow MCP server example patterns from official SDK
- Use basic-memory as reference for storage patterns

### Security Considerations
- Never commit `.env` or actual memory files
- Memory files stored locally (user's machine)
- No external API calls without user consent
- Sanitize file paths to prevent directory traversal

### Performance Considerations
- Lazy-load embeddings (don't generate on every save)
- Index conversations in background
- Cache frequent searches
- Limit embedding batch sizes

---

## Next Steps

1. **Get user approval** on this plan
2. **Clarify hooks system** - Research Claude Code hooks
3. **Choose embedding model** - Decide on model size/quality trade-off
4. **Begin scaffold** - Phase 1: Project initialization

---

## References

### Official Documentation
- MCP TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- MCP Server Example: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/src/simpleTaskInteractive.ts

### Inspiration Projects
- basic-memory: https://github.com/basicmachines-co/basic-memory
- mcp-memory: https://github.com/Puliczek/mcp-memory

### Dependencies
- `@modelcontextprotocol/server`: https://github.com/modelcontextprotocol/typescript-sdk
- `@xenova/transformers`: https://github.com/xenova/transformers.js
- `better-sqlite3`: https://github.com/WiseLibs/better-sqlite3

---

**Status:** Awaiting user approval to proceed with scaffold phase
