# iTerm2 Control Plugin

Bidirectional iTerm2 terminal control for Claude Code with seamless user handoff via tmux.

## Overview

This plugin enables Claude to create, control, and monitor terminal sessions in iTerm2, while also allowing users to take over control when needed. Perfect for running builds, executing tests, debugging, and collaborative terminal workflows.

## Features

- 🖥️ **Terminal Creation**: Spawn new iTerm2 tabs with commands
- 📊 **Output Monitoring**: Read terminal output with pagination
- 🔄 **Bidirectional Control**: Switch control between Claude and user
- 🤝 **tmux Integration**: Shared sessions for collaboration
- 📝 **Session Management**: Track and manage multiple sessions
- ⚡ **Real-time Monitoring**: Track long-running processes
- 🐛 **Interactive Debugging**: Create debugging sessions for user attachment

## Installation

### 1. Install Plugin from Marketplace

```bash
# Add marketplace (if not already added)
/plugin marketplace add tomerhamam/A2X-marketplace

# Install plugin
/plugin install iterm2-control@A2X
```

### 2. Enable iTerm2 Python API

**Critical**: iTerm2's Python API must be enabled for this to work.

1. Open iTerm2
2. Go to **Preferences** (⌘,)
3. Navigate to **General → Magic**
4. Enable **"Enable Python API"**
5. **Restart iTerm2**

### 3. Install Dependencies

```bash
cd /Users/tomerhamam/personal/projects/rmt-iterm2
pip3 install iterm2 mcp pydantic
```

### 4. Optional: Install tmux (for shared sessions)

```bash
brew install tmux
```

### 5. Restart Claude Code

Restart Claude Code to load the MCP server and plugin.

## Quick Start

### Create a Terminal

```bash
# Simple terminal
/create-terminal

# Run a command
/create-terminal npm start

# Python REPL
/create-terminal python -i
```

### Create a Shared Session

```bash
# For debugging
/shared-session debug-auth

# With initial command
/shared-session py-repl python -i

# Then attach from terminal:
tmux attach -t debug-auth
```

### List All Sessions

```bash
/list-terminals
```

## Usage Examples

### Example 1: Run Tests

**Ask Claude:**
> "Run the test suite and let me know if they pass"

**Claude will:**
1. Create terminal with `npm test`
2. Monitor output in real-time
3. Report results: passed/failed
4. Show errors if any
5. Clean up session

### Example 2: Monitor Build

**Ask Claude:**
> "Build the project for production and let me know when it's done"

**Claude will:**
1. Start build in new terminal
2. Report progress milestones
3. Detect completion or errors
4. Summarize build results
5. Report timing and size

### Example 3: Interactive Debugging

**Ask Claude:**
> "I'm getting an authentication error. Can you set up a debugging session?"

**Claude will:**
1. Create shared tmux session
2. Set up debugging environment
3. Provide attach command
4. You debug interactively
5. You detach (Ctrl+B, D)
6. Claude reads your debugging output
7. Discuss findings and implement fix

### Example 4: Long-Running Server

**Ask Claude:**
> "Start the development server and monitor it for errors"

**Claude will:**
1. Create terminal with dev server
2. Monitor logs continuously
3. Alert on errors or warnings
4. Keep session alive
5. You can take over control anytime

## Skills Reference

### run-and-monitor

Execute a command and monitor until completion.

**Use for:**
- Running tests
- Building projects
- Executing scripts
- Any command needing result verification

**Example:**
> "Run npm test and report results"

### debug-with-user

Create collaborative debugging session.

**Use for:**
- Complex bugs needing interaction
- Setting breakpoints
- Step-through debugging
- Real-time investigation

**Example:**
> "Help me debug the login function"

### monitor-build

Monitor long-running builds or processes.

**Use for:**
- Production builds
- Test suites
- Compilation
- CI/CD processes

**Example:**
> "Build the Docker image and let me know when done"

## Commands Reference

### /create-terminal [command]

Create a new iTerm2 terminal session.

```bash
/create-terminal              # Empty terminal
/create-terminal npm start    # Run command
/create-terminal python -i    # Python REPL
```

### /shared-session <name> [command]

Create a shared tmux session for collaboration.

```bash
/shared-session debug                    # Empty session
/shared-session py-debug python -i       # With command
/shared-session logs tail -f app.log     # Log monitoring
```

**Attach:** `tmux attach -t <name>`
**Detach:** `Ctrl+B`, then `D`

### /list-terminals

Show all active terminal sessions.

```bash
/list-terminals
```

Shows session ID, command, control mode, runtime, and line count.

## MCP Tools Available

When using Claude Code, you have direct access to these MCP tools:

### create_iterm_tab

Create a new iTerm2 tab with optional command.

```json
{
  "command": "npm test",
  "profile": "Default"
}
```

### send_to_session

Send text/commands to an active session.

```json
{
  "session_id": "uuid-here",
  "text": "ls -la\n"
}
```

### read_session_output

Read session output with pagination.

```json
{
  "session_id": "uuid-here",
  "offset": 0,
  "length": 100
}
```

### create_shared_session

Create a tmux session for user/Claude sharing.

```json
{
  "tmux_session": "debug-session",
  "command": "python -i"
}
```

### attach_user_to_session

Prepare a session for user attachment (provides tmux attach command).

```json
{
  "session_id": "uuid-here"
}
```

### list_sessions

List all active terminal sessions.

```json
{}
```

### terminate_session

Terminate and clean up a session.

```json
{
  "session_id": "uuid-here"
}
```

## Control Modes

Sessions have three control modes:

### Claude (`claude`)
- Created with `create_iterm_tab` (no tmux)
- Claude has exclusive control
- User can view but shouldn't interact
- **Use for:** Automated tasks, monitoring

### Shared (`shared`)
- Created with `create_shared_session`
- Both Claude and user can control
- User can attach/detach via tmux
- **Use for:** Debugging, collaboration, handoff

### User (`user`)
- Session handed off to user
- User has primary control
- Claude can still observe
- **Use for:** Manual intervention

## Workflows

### Workflow 1: Automated Task

```
1. User: "Run the linter"
2. Claude: create_iterm_tab(command="npm run lint")
3. Claude: Monitors output
4. Claude: Reports results
5. Claude: Terminates session
```

### Workflow 2: User Handoff

```
1. User: "I need to debug the API"
2. Claude: create_shared_session(tmux="api-debug")
3. Claude: Sends setup commands
4. Claude: "Attach with: tmux attach -t api-debug"
5. User: Attaches and debugs
6. User: Detaches (Ctrl+B, D)
7. Claude: Reads session output
8. Claude & User: Discuss findings
```

### Workflow 3: Long-Running Monitor

```
1. User: "Watch the build"
2. Claude: create_iterm_tab(command="npm run build")
3. Claude: Reports progress every 10s
4. Claude: Detects completion
5. Claude: Reports final status
6. Claude: Terminates session
```

## Troubleshooting

### "Failed to connect to iTerm2"

**Cause:** Python API not enabled or iTerm2 not running.

**Solution:**
1. Make sure iTerm2 is running
2. Enable Python API: Preferences > General > Magic > Enable "Python API"
3. Restart iTerm2
4. Restart Claude Code

### "tmux not available"

**Cause:** tmux not installed.

**Solution:**
```bash
brew install tmux
```

### Session Not Found

**Cause:** Session was terminated or doesn't exist.

**Solution:**
- Use `/list-terminals` to see active sessions
- Create new session with `/create-terminal` or `/shared-session`

### Can't Attach to tmux Session

**Cause:** Wrong session name or tmux not running.

**Solution:**
```bash
# List all tmux sessions
tmux ls

# Attach to specific session
tmux attach -t session-name
```

## Best Practices

### Session Naming (tmux)
- ✅ Use descriptive names: `debug-auth`, `build-prod`
- ✅ Lowercase with hyphens
- ✅ Indicate purpose: `test-runner`, `dev-server`
- ❌ Avoid: `temp`, `session1`, `DEBUG`

### Control Mode Selection
- Use **claude** for: Automated tasks, builds, tests
- Use **shared** for: Debugging, exploration, collaboration
- Switch to **user** when: Manual intervention needed

### Resource Management
- Always terminate sessions when done
- Don't leave builds running indefinitely
- Use `/list-terminals` to check active sessions
- Clean up old sessions periodically

### Error Handling
- Claude will report errors immediately
- Read full error context with pagination
- Use shared sessions for complex debugging
- Let Claude suggest fixes based on errors

## Requirements

- **iTerm2**: Build 3.3.0 or later
- **Python**: 3.9+
- **Packages**: iterm2, mcp, pydantic
- **tmux**: Optional (for shared sessions)
- **macOS**: Required (iTerm2 is macOS-only)

## Source Code

The iTerm2 MCP Server source is at:
```
/Users/tomerhamam/personal/projects/rmt-iterm2
```

See the server README for implementation details and development info.

## Support

For issues or questions:
- Check TESTING.md in the server repo
- Review troubleshooting section above
- Run installation test: `python3 test_installation.py`

## License

[Your License Here]

## Credits

Built with:
- [iTerm2 Python API](https://iterm2.com/python-api/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [tmux](https://github.com/tmux/tmux)
