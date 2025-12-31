# mactools

macOS terminal automation with iTerm2 MCP server for command execution, session management, and collaborative debugging.

## Overview

mactools is a Claude Code plugin that provides powerful terminal automation capabilities for macOS through the iTerm2 MCP (Model Context Protocol) server. It enables seamless control of iTerm2 from Claude Code, allowing you to create terminals, execute commands, monitor output, and collaborate with users through shared tmux sessions.

## Features

- **Terminal Creation** - Programmatically create iTerm2 tabs with custom commands
- **Command Execution** - Send commands and text to terminal sessions
- **Output Monitoring** - Read terminal output with pagination and offset support
- **Session Management** - Track and manage multiple concurrent terminal sessions
- **Collaborative Sessions** - Use tmux for user/AI handoff and shared control
- **Session Persistence** - tmux sessions survive disconnections and can be reattached
- **Multiple Control Modes** - Claude-controlled, user-controlled, or shared sessions

## Installation

### Prerequisites

1. **iTerm2** (build 3.3.0 or later)
2. **Python 3.9+**
3. **tmux** (optional, for shared sessions)
   ```bash
   brew install tmux
   ```

### Step 1: Enable iTerm2 Python API

**Critical**: This must be done for the MCP server to work.

1. Open iTerm2
2. Go to **Preferences** (⌘,)
3. Navigate to **General** → **Magic**
4. Enable **"Enable Python API"**
5. **Restart iTerm2**

### Step 2: Install iTerm2 MCP Server

```bash
cd /Users/tomerhamam/personal/projects/rmt-iterm2
pip3 install -e .
```

### Step 3: Install mactools Plugin

```bash
# Add A2X marketplace
/plugin marketplace add tomerhamam/A2X-marketplace

# Install mactools
/plugin install mactools@A2X
```

### Step 4: Restart Claude Code

Restart Claude Code to load the plugin and MCP server.

### Step 5: Verify Installation

Test in a Claude Code session:

```
User: "Create a new terminal tab"
Claude: [Uses create_iterm_tab tool]
```

If successful, a new iTerm2 tab will open.

## Available Tools

The iTerm2 MCP server provides 7 tools for terminal control:

### 1. create_iterm_tab

Create a new iTerm2 tab with optional command and tmux session.

**Parameters:**
- `command` (optional): Shell command to execute
- `tmux_session` (optional): tmux session name for persistence
- `profile` (optional): iTerm2 profile name

**Example:**
```python
create_iterm_tab(command="npm test")
create_iterm_tab(command="python server.py", profile="Development")
```

### 2. create_shared_session

Create a tmux session for user/Claude sharing.

**Parameters:**
- `tmux_session`: Session name
- `command` (optional): Initial command to run

**Example:**
```python
create_shared_session(tmux_session="debugging", command="python debug.py")
```

### 3. send_to_session

Send text or commands to an active session.

**Parameters:**
- `session_id`: Session UUID
- `text`: Text to send (include `\n` for execution)

**Example:**
```python
send_to_session(session_id="uuid-1234", text="ls -la\n")
```

### 4. read_session_output

Read output from a session with pagination.

**Parameters:**
- `session_id`: Session UUID
- `offset` (default: 0): Starting line (0=new, positive=absolute, negative=tail)
- `length` (default: 1000): Maximum lines to return

**Example:**
```python
read_session_output(session_id="uuid", offset=0, length=100)
read_session_output(session_id="uuid", offset=-50, length=50)  # Last 50 lines
```

### 5. list_sessions

List all active sessions with details.

**Returns:** Session ID, command, control mode, runtime, line count

### 6. attach_user_to_session

Prepare a session for user attachment (requires tmux).

**Parameters:**
- `session_id`: Session UUID

**Returns:** tmux attach command for the user

### 7. terminate_session

Terminate a session and clean up resources.

**Parameters:**
- `session_id`: Session UUID

## Usage Examples

### Example 1: Run Tests and Check Results

```
User: "Run the test suite and tell me if it passes"

Claude: "I'll run the tests and analyze the results."

[Claude creates a terminal and runs tests]
[Waits for completion]
[Reads output and analyzes]

Claude: "✅ All 47 tests passed!
  - Unit tests: 32 passed
  - Integration tests: 15 passed
  - Total time: 12.3s"
```

### Example 2: Collaborative Debugging

```
User: "I need to debug the authentication flow"

Claude: "I'll set up an interactive debugging session."

[Creates shared tmux session with debugger]

Claude: "Created shared session 'auth-debug'.

To attach:
  tmux attach -t auth-debug

I've set a breakpoint at the login function.
When done debugging, detach with: Ctrl+B, then D"

[User attaches, debugs, detaches]

Claude: "I can see from your debugging that the issue is
the password hash comparison using the wrong salt..."
```

### Example 3: Monitor Long-Running Build

```
User: "Start the production build and monitor it"

Claude: "I'll start the build and track progress."

[Creates terminal with build command]
[Polls output every 15 seconds]

Claude: "⏳ Build in progress (1m 30s):
  ✓ TypeScript compiled
  ✓ Assets bundled
  ⏳ Running optimizations..."

[Later]

Claude: "✅ Build completed! (2m 45s)
  - Bundle size: 2.4 MB
  - Output: dist/
  - No errors or warnings"
```

### Example 4: Setup Development Environment

```
User: "Set up the development environment"

Claude: "I'll start all required services."

[Creates multiple terminals]
1. Server: npm run dev
2. Database: docker-compose up postgres
3. Redis: docker-compose up redis

Claude: "✅ Environment ready!
  ✓ Server - http://localhost:3000
  ✓ Database - localhost:5432
  ✓ Redis - localhost:6379"
```

## Workflows

### Workflow 1: Automated Testing

```python
# 1. Create tab and run tests
result = create_iterm_tab(command="npm test")
session_id = result["session_id"]

# 2. Wait for tests
time.sleep(5)

# 3. Read results
output = read_session_output(session_id=session_id)

# 4. Analyze and report
if "All tests passed" in output["output"]:
    print("✅ Tests passed!")
```

### Workflow 2: User Handoff

```python
# 1. Create shared session
result = create_shared_session(
    tmux_session="debug-session",
    command="python app.py"
)

# 2. Set up debugging
send_to_session(result["session_id"], "import pdb; pdb.set_trace()\n")

# 3. Hand off to user
attach_user_to_session(result["session_id"])

# 4. User debugs, then detaches

# 5. Claude resumes monitoring
output = read_session_output(session_id=result["session_id"])
```

### Workflow 3: Multi-Service Setup

```python
# Start multiple services in parallel
services = []

for service in ["server", "database", "worker"]:
    result = create_iterm_tab(command=f"npm run {service}")
    services.append({
        "name": service,
        "session_id": result["session_id"]
    })

# Monitor all services
for svc in services:
    output = read_session_output(svc["session_id"])
    print(f"{svc['name']}: Running")
```

## Control Modes

Sessions operate in three control modes:

### Claude Mode
- Claude has exclusive control
- Default for non-tmux sessions
- Best for automated tasks

### Shared Mode
- Both Claude and user can control
- Used for tmux sessions
- Best for collaborative work
- Claude warns before sending commands

### User Mode
- User has taken control
- Claude can still read output
- User can return control by detaching

## Skills

### Terminal Automation

Automated terminal workflows for testing, building, and monitoring.

**Use cases:**
- Run test suites and analyze results
- Monitor build processes
- Execute multi-step deployments
- Setup development environments

**Automatic detection:**
- "Run the tests and let me know"
- "Start the build and monitor it"
- "Execute the deployment script"

### Collaborative Debug

Interactive debugging sessions with user handoff.

**Use cases:**
- Debug complex issues together
- Interactive debugging (pdb, node inspect)
- Pair programming
- Production issue investigation

**Automatic detection:**
- "Help me debug [issue]"
- "Set up a debugging session"
- "Let me take control to investigate"

## Commands

### Terminal Creation

Create new terminal tabs quickly:

```bash
# Examples
"Create a new terminal"
"Run npm test in a new terminal"
"Start the development server in a new tab"
```

### Shared Sessions

Create collaborative sessions:

```bash
# Examples
"Create a shared debugging session"
"Set up a tmux session I can attach to"
"Create a collaborative terminal for [task]"
```

## Best Practices

### ✅ Do This

- **Use tmux for shared sessions** - Reliable output and user handoff
- **Set appropriate wait times** - Give commands time to complete
- **Poll efficiently** - Don't spam read_session_output
- **Clean up sessions** - Terminate when done
- **Use descriptive session names** - Easy to identify
- **Provide clear user instructions** - How to attach/detach

### ❌ Avoid This

- **Don't poll too frequently** - Wastes resources
- **Don't leave sessions running** - Clean up when done
- **Don't use generic names** - Be specific
- **Don't assume success** - Always check output
- **Don't rely on non-tmux output** - Use tmux for reliability

## Troubleshooting

### "Failed to connect to iTerm2"

**Cause:** iTerm2 Python API not enabled or iTerm2 not running.

**Solution:**
1. Ensure iTerm2 is running
2. Enable Python API: Preferences → General → Magic
3. Restart iTerm2
4. Restart Claude Code

### "tmux requested but not available"

**Cause:** tmux is not installed.

**Solution:**
```bash
brew install tmux
```

### "Session not found"

**Cause:** Session was terminated or doesn't exist.

**Solution:**
- Use `list_sessions()` to see active sessions
- Create a new session

### Server doesn't appear in Claude Code

**Cause:** MCP configuration issue.

**Solution:**
1. Verify plugin is installed: `/plugin list`
2. Check `mcp-config.json` has correct path
3. Restart Claude Code
4. Check logs for errors

### Output is empty

**Cause:** Non-tmux sessions have limited buffering.

**Solution:**
- Use tmux sessions: `create_shared_session()`
- For reliable output capture

## Advanced Usage

### Custom iTerm2 Profiles

```python
# Use different profiles for different tasks
create_iterm_tab(command="npm start", profile="Development")
create_iterm_tab(command="ssh prod", profile="Production")
```

### Multiple Concurrent Sessions

```python
# Track multiple processes
sessions = []
for project in ["api", "web", "mobile"]:
    result = create_iterm_tab(command=f"cd {project} && npm run build")
    sessions.append({"project": project, "id": result["session_id"]})

# Monitor all
for s in sessions:
    output = read_session_output(s["id"])
    print(f"{s['project']}: {output['total_lines']} lines")
```

### Session Recovery

```python
# List all sessions
all_sessions = list_sessions()

# Find specific session
target = next(s for s in all_sessions["sessions"]
              if "pytest" in s.get("command", ""))

# Read its output
output = read_session_output(target["session_id"])
```

## Technical Details

### Architecture

```
┌─────────────┐
│ Claude Code │
└──────┬──────┘
       │ MCP Protocol
┌──────▼──────────────┐
│ iTerm2 MCP Server   │
│  - Session Manager  │
│  - Output Buffer    │
│  - tmux Integration │
└──────┬──────────────┘
       │
   ┌───┴───┬────────┬────────┐
   │       │        │        │
┌──▼──┐ ┌─▼───┐ ┌──▼────┐ ┌─▼──┐
│iTerm│ │tmux │ │Process│ │API │
└─────┘ └─────┘ └───────┘ └────┘
```

### Session Management

Each session tracks:
- UUID (unique identifier)
- Command (original command)
- Control mode (claude/shared/user)
- tmux session (if applicable)
- Output buffer
- Read offset
- Runtime

### Output Buffering

- **tmux sessions**: Full output capture
- **non-tmux sessions**: Limited buffering
- **Pagination**: offset + length
- **Tail support**: negative offset

## Version History

- **v1.0.0** (2025-01-XX)
  - Initial release
  - iTerm2 MCP server integration
  - 7 core terminal control tools
  - tmux support for shared sessions
  - Terminal automation workflows
  - Collaborative debugging support

## Related Resources

- [iTerm2 Python API](https://iterm2.com/python-api/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [tmux Documentation](https://github.com/tmux/tmux/wiki)
- [iTerm2 MCP Server Source](file:///Users/tomerhamam/personal/projects/rmt-iterm2)

## Support

**Maintainer:** Tomer Hamam (tomerhamam@gmail.com)
**MCP Server:** `/Users/tomerhamam/personal/projects/rmt-iterm2`

## License

MIT License

---

**Quick Start:**

```bash
# 1. Enable iTerm2 Python API
#    Preferences > General > Magic > Enable "Python API" > Restart iTerm2

# 2. Install MCP server
cd /Users/tomerhamam/personal/projects/rmt-iterm2
pip3 install -e .

# 3. Install plugin
/plugin marketplace add tomerhamam/A2X-marketplace
/plugin install mactools@A2X

# 4. Test
"Create a new terminal and run echo 'Hello from mactools!'"
```
