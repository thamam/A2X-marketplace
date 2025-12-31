# THH10x Tools

Advanced terminal control and automation toolkit featuring the iTerm2 MCP server for bidirectional terminal management, command execution, and session sharing.

## Overview

THH10x is a comprehensive plugin that provides powerful terminal automation capabilities through the iTerm2 MCP (Model Context Protocol) server. It enables Claude Code to:

- **Create and manage iTerm2 tabs** programmatically
- **Execute commands** and monitor their output
- **Hand off control** to users via tmux sessions
- **Share terminal sessions** between Claude and users
- **Read terminal output** with pagination and offset support
- **Track multiple sessions** concurrently

## Core Component: iTerm2 MCP Server

The centerpiece of this plugin is the iTerm2 MCP server, a sophisticated integration that bridges Claude Code with iTerm2's Python API. This enables seamless terminal automation and collaborative workflows.

### Key Features

#### 🖥️ Direct iTerm2 Control
- Create new tabs with custom profiles
- Send commands programmatically
- Manage session lifecycle

#### 🔄 Bidirectional Handoff
- Switch control between Claude and user
- Use tmux for persistent sessions
- Collaborative debugging and monitoring

#### 📊 Output Management
- Read terminal output with pagination
- Support for offset-based reading (head/tail)
- Track line counts and session state

#### 🔧 Session Persistence
- tmux integration for long-running processes
- Sessions survive reconnections
- User can detach and reattach anytime

#### 🎯 Control Modes
- **Claude mode**: Exclusive AI control
- **Shared mode**: Both AI and user can control
- **User mode**: User has taken over

## Installation

### Prerequisites

1. **iTerm2** (build 3.3.0 or later)
2. **Python 3.9+**
3. **tmux** (optional, for shared sessions)
   ```bash
   brew install tmux
   ```

### From A2X Marketplace

```bash
# Add the A2X marketplace
/plugin marketplace add tomerhamam/A2X-marketplace

# Install thh10x
/plugin install thh10x@A2X
```

### Setup Steps

#### 1. Enable iTerm2 Python API (CRITICAL)

This is **required** for the MCP server to work:

1. Open iTerm2
2. Go to **Preferences** (⌘,)
3. Navigate to **General** → **Magic**
4. Enable **"Enable Python API"**
5. **Restart iTerm2**

#### 2. Install MCP Server Dependencies

```bash
cd /Users/tomerhamam/personal/projects/rmt-iterm2
pip3 install -e .
```

#### 3. Configure MCP Server

Add to `~/.config/claude-code/mcp.json`:

```json
{
  "mcpServers": {
    "iterm2": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/Users/tomerhamam/personal/projects/rmt-iterm2",
      "env": {}
    }
  }
}
```

#### 4. Restart Claude Code

Restart Claude Code to load the MCP server.

#### 5. Verify Installation

Test in a Claude Code session:

```
User: "Create a new terminal tab"
Claude: [Uses create_iterm_tab tool]
```

If successful, a new iTerm2 tab will open.

## Available Tools

The iTerm2 MCP server provides 7 tools:

### 1. create_iterm_tab

Create a new iTerm2 tab with optional command and tmux session.

**Parameters:**
- `command` (optional): Shell command to execute
- `tmux_session` (optional): tmux session name for persistence
- `profile` (optional): iTerm2 profile name

**Example:**
```python
create_iterm_tab(command="npm test")
create_iterm_tab(command="python server.py", profile="Hotkey Window")
```

### 2. create_shared_session

Create a tmux session for user/Claude sharing.

**Parameters:**
- `tmux_session`: Session name for tmux
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
# Read new output
read_session_output(session_id="uuid")

# Read last 50 lines
read_session_output(session_id="uuid", offset=-50, length=50)
```

### 5. list_sessions

List all active sessions.

**Returns:** Session details including ID, command, control mode, runtime, line count

**Example:**
```python
list_sessions()
```

### 6. attach_user_to_session

Prepare a session for user attachment (requires tmux).

**Parameters:**
- `session_id`: Session UUID

**Example:**
```python
attach_user_to_session(session_id="uuid")
# Returns: "tmux attach -t session-name"
```

### 7. terminate_session

Terminate a session and clean up resources.

**Parameters:**
- `session_id`: Session UUID

**Example:**
```python
terminate_session(session_id="uuid")
```

## Workflows

### Workflow 1: Run Tests and Check Results

```python
# 1. Create a tab and run tests
result = create_iterm_tab(command="npm test")
session_id = result["session_id"]

# 2. Wait for tests to run
time.sleep(3)

# 3. Read the output
output = read_session_output(session_id=session_id)

# 4. Check results
if "All tests passed" in output["output"]:
    print("✅ Tests passed!")
else:
    print("❌ Tests failed - check output")
```

### Workflow 2: Collaborative Debugging

```python
# 1. Create a shared session
result = create_shared_session(
    tmux_session="debug-session",
    command="python app.py"
)
session_id = result["session_id"]

# 2. Claude runs initial commands
send_to_session(session_id, "import pdb; pdb.set_trace()\n")

# 3. Hand off to user
handoff = attach_user_to_session(session_id)
print(f"User can attach with: {handoff['attach_command']}")

# 4. User debugs interactively, then detaches (Ctrl+B, D)

# 5. Claude can resume monitoring
output = read_session_output(session_id=session_id)
```

### Workflow 3: Monitor Long-Running Build

```python
# 1. Start the build
result = create_iterm_tab(command="./build.sh")
session_id = result["session_id"]

# 2. Periodically check progress
while True:
    output = read_session_output(session_id)

    if "BUILD SUCCESSFUL" in output["output"]:
        print("✅ Build completed!")
        break
    elif "ERROR" in output["output"]:
        print("❌ Build failed!")
        # Read full output to diagnose
        break

    time.sleep(10)  # Check every 10 seconds
```

### Workflow 4: Setup Development Environment

```python
# 1. Create a new tab for the server
server_tab = create_iterm_tab(command="npm run dev")

# 2. Create another tab for database
db_tab = create_iterm_tab(command="docker-compose up postgres")

# 3. Create a shared session for interactive work
work_session = create_shared_session(
    tmux_session="dev-work",
    command="cd src && clear"
)

# User can now: tmux attach -t dev-work
```

## Components

### Skills

#### terminal-automation
Automated terminal workflows using iTerm2 control for testing, building, and monitoring.

**Use cases:**
- Run test suites and analyze results
- Monitor build processes
- Execute multi-step deployment workflows

#### collaborative-debug
Set up collaborative debugging sessions using tmux where Claude and user can both interact with the terminal.

**Use cases:**
- Debug production issues together
- Pair programming sessions
- Training and knowledge transfer

### Commands

#### /create-terminal
Create a new iTerm2 terminal tab or session.

**Usage:**
```bash
/create-terminal          # New tab with shell
/create-terminal npm test # New tab running tests
```

#### /shared-session
Create a shared tmux session for collaboration.

**Usage:**
```bash
/shared-session debug     # Creates tmux session named "debug"
```

## Control Modes Explained

Sessions have three control modes:

### Claude Mode (Default for non-tmux)
- Claude has exclusive control
- User should not type in this tab
- Best for automated tasks

### Shared Mode (tmux sessions)
- Both Claude and user can control
- Claude warns before sending commands
- User can attach/detach anytime
- Best for collaborative work

### User Mode (Informational)
- User has taken over
- Claude can still read output
- Claude avoids sending commands
- User can return control by detaching

## Troubleshooting

### "Failed to connect to iTerm2"

**Cause:** iTerm2 Python API not enabled or iTerm2 not running.

**Solution:**
1. Ensure iTerm2 is running
2. Enable Python API: **Preferences** → **General** → **Magic**
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
- Create a new session with `create_iterm_tab()`

### Server doesn't appear in Claude Code

**Cause:** MCP configuration issue.

**Solution:**
1. Verify `~/.config/claude-code/mcp.json` has correct path
2. Check Python interpreter is accessible
3. Restart Claude Code
4. Check for errors in Claude Code logs

### Output is empty when reading session

**Cause:** Non-tmux sessions have limited output buffering.

**Solution:**
- Use tmux sessions for reliable output: `create_shared_session()`
- For non-tmux, output may not be available

## Best Practices

### ✅ Do This

- **Use tmux for shared sessions** - Reliable output capture and user handoff
- **Create descriptive tmux session names** - Easy to find and attach
- **Read output periodically** - Don't overwhelm with constant polling
- **Terminate sessions when done** - Clean up resources
- **Use appropriate control modes** - Match the workflow

### ❌ Avoid This

- **Don't create too many sessions** - Clean up when done
- **Don't rely on non-tmux output** - Use tmux for reliable capture
- **Don't send rapid-fire commands** - Give time for execution
- **Don't ignore control mode warnings** - User may be typing

## Advanced Usage

### Custom iTerm2 Profiles

Create specialized profiles in iTerm2 for different tasks:

```python
# Development profile with specific theme
create_iterm_tab(command="npm start", profile="Development")

# Production profile with different colors
create_iterm_tab(command="ssh prod-server", profile="Production")
```

### Multiple Concurrent Sessions

Track multiple long-running processes:

```python
# Start multiple builds
sessions = []
for project in ["api", "web", "mobile"]:
    result = create_iterm_tab(command=f"cd {project} && npm run build")
    sessions.append({
        "project": project,
        "session_id": result["session_id"]
    })

# Monitor all builds
for s in sessions:
    output = read_session_output(s["session_id"])
    print(f"{s['project']}: {output['total_lines']} lines")
```

### Session Recovery

List and reconnect to existing sessions:

```python
# List all sessions
all_sessions = list_sessions()

# Find a specific session
target = next(s for s in all_sessions["sessions"]
              if "pytest" in s.get("command", ""))

# Read its output
output = read_session_output(target["session_id"])
```

## Examples

### Example 1: Automated Testing

```
User: "Run the test suite and let me know if it passes"

Claude: "I'll create a terminal session and run the tests."

[Creates tab with npm test, waits, reads output]

Claude: "✅ All 47 tests passed! Here's the summary:
  - Unit tests: 32 passed
  - Integration tests: 15 passed
  - Total time: 12.3s"
```

### Example 2: Debugging Handoff

```
User: "I need to debug the authentication flow"

Claude: "I'll set up a debugging session you can attach to."

[Creates shared tmux session with the app running]

Claude: "I've created a tmux session 'auth-debug' with the app running.
You can attach with: tmux attach -t auth-debug

I've already set a breakpoint at the login function. When you're done
debugging, detach with Ctrl+B then D, and I can continue monitoring."
```

### Example 3: Build Monitoring

```
User: "Start the production build and monitor it"

Claude: "I'll start the build and watch for completion."

[Creates tab, runs build, polls output]

Claude: "⏳ Build in progress... (2m 15s elapsed)
  ✓ Compiled TypeScript
  ✓ Bundled assets
  ⏳ Running optimizations..."

[Later]

Claude: "✅ Build completed successfully! (Total time: 3m 42s)
  - Bundle size: 2.4 MB
  - Output: dist/
  - No warnings or errors"
```

## Technical Details

### Architecture

```
┌─────────────┐
│ Claude Code │
└──────┬──────┘
       │
       │ MCP Protocol
       │
┌──────▼──────────────┐
│ iTerm2 MCP Server   │
│  - Session Manager  │
│  - Output Buffer    │
│  - tmux Integration │
└──────┬──────────────┘
       │
       ├─────────┬────────────┐
       │         │            │
   ┌───▼───┐ ┌──▼────┐  ┌───▼────┐
   │iTerm2 │ │ tmux  │  │Process │
   │  API  │ │Session│  │Spawning│
   └───────┘ └───────┘  └────────┘
```

### Session Management

Each session tracks:
- **UUID**: Unique identifier
- **Command**: Original command executed
- **Control mode**: claude/shared/user
- **tmux session**: If using tmux
- **Output buffer**: Captured lines
- **Read offset**: Last read position
- **Runtime**: Session duration

### Output Buffering

- **tmux sessions**: Full output capture via tmux buffer
- **non-tmux sessions**: Limited buffering (implementation-dependent)
- **Pagination**: Offset + length for efficient reading
- **Tail support**: Negative offset reads from end

## Version History

- **v1.0.0** (2025-01-XX)
  - Initial release
  - iTerm2 MCP server integration
  - 7 core tools for terminal control
  - tmux support for shared sessions
  - Terminal automation skill
  - Collaborative debug skill

## Related Resources

- [iTerm2 Python API Documentation](https://iterm2.com/python-api/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [tmux Documentation](https://github.com/tmux/tmux/wiki)
- [Claude Code Docs](https://code.claude.com/docs)

## Support

**Issues:** GitHub repository
**Maintainer:** Tomer Hamam (tomerhamam@gmail.com)
**MCP Server Source:** `/Users/tomerhamam/personal/projects/rmt-iterm2`

## Contributing

To extend this plugin:

1. **Add new skills:**
   - Create `skills/your-skill.md`
   - Update `plugin.json` components.skills
   - Document in README

2. **Add new commands:**
   - Create `commands/your-command.md`
   - Update `plugin.json` components.commands
   - Add usage examples

3. **Improve MCP server:**
   - See `rmt-iterm2` repository
   - Submit PRs for new features
   - Update plugin documentation

## License

MIT License - See parent repository for details

---

**Quick Start:**

```bash
# 1. Enable iTerm2 Python API (Preferences > General > Magic)
# 2. Install
/plugin marketplace add tomerhamam/A2X-marketplace
/plugin install thh10x@A2X

# 3. Configure MCP server in ~/.config/claude-code/mcp.json
# 4. Restart Claude Code

# 5. Test
"Create a new terminal tab and run 'echo Hello from THH10x!'"
```
