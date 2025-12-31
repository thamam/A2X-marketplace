# A2X Marketplace

My useful Claude Code plugins that I can install on demand when I need them.

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add tomerhamam/A2X-marketplace
```

## Available Plugins

### thh10x (v1.0.0)

Advanced terminal control and automation toolkit featuring the iTerm2 MCP server.

**Features:**
- 🖥️ **Direct iTerm2 Control** - Create tabs, send commands, and manage sessions
- 🔄 **Bidirectional Handoff** - Switch control between Claude and user via tmux
- 📊 **Output Management** - Read terminal output with pagination and offset support
- 🔧 **Session Persistence** - tmux integration for long-running processes
- 🤖 **Terminal Automation** - Automated test execution, build monitoring, and workflows
- 🐛 **Collaborative Debug** - Interactive debugging sessions with user handoff

**Install:**
```bash
/plugin install thh10x@A2X
```

**Quick Start:**
```bash
/create-terminal npm test       # Create terminal and run tests
/shared-session debug           # Create collaborative debugging session
```

**Requirements:**
- iTerm2 with Python API enabled (Preferences > General > Magic)
- Python 3.9+
- iTerm2 MCP server from `/Users/tomerhamam/personal/projects/rmt-iterm2`
- Optional: `tmux` for shared sessions (`brew install tmux`)

[Full Documentation →](./plugins/thh10x/README.md)

---

### mactools (v1.0.0)

macOS terminal automation with iTerm2 MCP server for command execution and session management.

**Features:**
- 🖥️ **Terminal Creation** - Create iTerm2 tabs with custom commands
- 📊 **Output Monitoring** - Read terminal output with pagination
- 🔄 **Session Management** - Track and manage multiple sessions
- 🤝 **tmux Integration** - Shared sessions for collaboration
- 🤖 **Terminal Automation** - Automated testing and build monitoring
- 🐛 **Collaborative Debug** - Interactive debugging with user handoff

**Install:**
```bash
/plugin install mactools@A2X
```

**Quick Start:**
```
"Create a new terminal and run npm test"
"Create a shared debugging session"
"Monitor the build process"
```

**Requirements:**
- iTerm2 with Python API enabled (Preferences > General > Magic)
- Python 3.9+
- iTerm2 MCP server installed
- Optional: `tmux` for shared sessions (`brew install tmux`)

**Setup:**
```bash
# Install iTerm2 MCP server
cd /Users/tomerhamam/personal/projects/rmt-iterm2
pip3 install -e .
```

[Full Documentation →](./plugins/mactools/README.md)

---

### iterm2-control (v1.0.0)

Bidirectional iTerm2 terminal control with seamless user handoff via tmux.

**Features:**
- 🖥️ **Terminal Creation** - Spawn new iTerm2 tabs with commands
- 📊 **Output Monitoring** - Read terminal output with pagination
- 🔄 **Bidirectional Control** - Switch control between Claude and user
- 🤝 **tmux Integration** - Shared sessions for collaboration
- 🐛 **Interactive Debugging** - Create debugging sessions for user attachment

**Install:**
```bash
/plugin install iterm2-control@A2X
```

**Quick Start:**
```bash
/create-terminal npm test       # Run tests and monitor
/shared-session debug           # Create collaborative session
/list-terminals                 # Show all active sessions
```

**Requirements:**
- iTerm2 with Python API enabled (Preferences > General > Magic)
- Python packages: `iterm2`, `mcp`, `pydantic`
- Optional: `tmux` for shared sessions (`brew install tmux`)

[Full Documentation →](./plugins/iterm2-control/README.md)

---

### maya-toolkit (v1.0.0)

Comprehensive development workflow automation for Maya AI projects.

**Features:**
- 🎯 **Task Planner** - Research, scope, and break down tasks with Linear integration
- 📝 **PR Walkthrough** - Generate navigational review guides for Theia tool
- 📚 **Documentation Specialist** - Automated inline and comprehensive documentation
- 🔄 **Session Management** - Handoff and resume workflows for context continuity

**Install:**
```bash
/plugin install maya-toolkit@A2X
```

**Quick Start:**
```bash
/prepare-task PRO-123           # Prepare and scope a Linear task
/create-theia-inputs            # Generate PR walkthrough
/session-handoff                # Create session handoff document
```

**Requirements:**
- Linear API key (`LINEAR_API_KEY` environment variable)
- Linear MCP server configured
- Git worktrees support

[Full Documentation →](./plugins/maya-toolkit/README.md)

---

### claude-memory (v1.0.0)

Persistent memory management with conversation history, knowledge base, and semantic search.

**Features:**
- 💾 **Conversation History** - Store and retrieve past conversations
- 📚 **Knowledge Base** - Build searchable knowledge from interactions
- 🔄 **Session Persistence** - Save/restore complete session state
- 🔍 **Semantic Search** - Vector-based memory retrieval (works locally!)
- 🏠 **Local-First** - Everything stored on your machine, no external services
- 🔒 **Privacy-First** - Your data never leaves your machine

**Install:**
```bash
/plugin install claude-memory@A2X
```

**Quick Start:**
```bash
/remember Project Preferences | Use pnpm for package management tags: workflow
/recall pnpm workflow
/save-conversation React hooks discussion
/search-knowledge authentication patterns
```

**Requirements:**
- Node.js >= 20.0.0
- ~500MB disk space (model + memories)
- First run downloads embedding model (~80-420MB depending on choice)

**Setup:**
```bash
cd ~/.claude-code/plugins/claude-memory/mcp-server
npm install && npm run build
```

[Full Documentation →](./plugins/claude-memory/README.md)

---

## RTL Language Support (Hebrew/Arabic)

Having issues with Hebrew text displaying incorrectly in Claude Code?

**Quick Fix for iTerm2:**
1. Open iTerm2 Preferences (⌘,)
2. Navigate to: Settings > General > Experimental
3. Enable: "Enable support for right-to-left scripts"
4. Restart iTerm2

**RTL Utilities (auto-loaded in your shell):**
```bash
# ALL your Claude Code aliases now have Hebrew (-he) versions!
claude-free-he "שאלה"       # claude-free with RTL ⭐ Most used
happy-free-he "שאלה"        # happy-free with RTL
happy-he "שאלה"             # happy with RTL
happy-codex-he "שאלה"       # codex mode with RTL
happy-resume-he             # resume session with RTL
# ... and 20+ more! See complete list below

# Standalone RTL functions
rtl_print "שלום עולם"       # Right-align text
center_print "כותרת"         # Center-align
echo "text" | rtl_block      # Multi-line right-align
```

**Resources:**
- [Complete Alias List →](./RTL_CLAUDE_ALIASES.md) - **All Hebrew wrappers** ⭐
- [Claude Code Integration →](./RTL_WITH_CLAUDE_CODE.md) - Use with Happy/Claude
- [Quick Cheatsheet →](./RTL_CHEATSHEET.md) - Fast reference
- [Usage Guide →](./RTL_USAGE_GUIDE.md) - Detailed examples
- [Full RTL Support Guide →](./RTL_HEBREW_SUPPORT_GUIDE.md) - Complete documentation

---

## Usage

Install plugins from this marketplace:

```bash
/plugin install <plugin-name>@A2X
```

## Maintainer

Tomer Hamam (tomerhamam@gmail.com)
