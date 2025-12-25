# A2X Marketplace

My useful Claude Code plugins that I can install on demand when I need them.

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add tomerhamam/A2X-marketplace
```

## Available Plugins

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

## Usage

Install plugins from this marketplace:

```bash
/plugin install <plugin-name>@A2X
```

## Maintainer

Tomer Hamam (tomerhamam@gmail.com)
