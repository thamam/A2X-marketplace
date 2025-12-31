# /create-terminal

Create a new iTerm2 terminal tab or session with optional command execution.

## Usage

```bash
/create-terminal                          # New tab with default shell
/create-terminal npm test                 # New tab running tests
/create-terminal python server.py         # New tab running Python server
/create-terminal --profile Development    # New tab with specific profile
```

## Description

This command creates a new iTerm2 terminal tab using the iTerm2 MCP server. You can optionally specify a command to run immediately in the new tab, or create an empty tab with the default shell.

## Parameters

- **command** (optional): Shell command to execute in the new tab
- **--profile** (optional): iTerm2 profile name to use for the tab
- **--tmux** (optional): Create as a tmux session with the given name

## Examples

### Basic Usage

```bash
# Create empty tab
/create-terminal

# Run tests in new tab
/create-terminal npm test

# Start development server
/create-terminal npm run dev

# Run Python script
/create-terminal python manage.py runserver
```

### With Profiles

```bash
# Use specific iTerm2 profile
/create-terminal --profile "Hotkey Window" htop

# Development profile for server
/create-terminal --profile Development npm start
```

### With tmux

```bash
# Create tmux session for persistence
/create-terminal --tmux dev-server npm start

# User can later attach with: tmux attach -t dev-server
```

## When to Use

Use this command when you need to:
- Quickly create a new terminal for a specific task
- Run a command in a separate terminal window
- Set up a dedicated terminal for monitoring
- Create multiple terminals for different services
- Test commands in isolation

## Output

The command will:
1. Create a new iTerm2 tab
2. Optionally run the specified command
3. Return a session_id for programmatic control
4. Show the command being executed (if any)

## Related

- `/shared-session` - Create a tmux session for collaboration
- `terminal-automation` skill - For automated terminal workflows
- `collaborative-debug` skill - For interactive debugging sessions

## Notes

- Requires iTerm2 with Python API enabled
- The iTerm2 MCP server must be configured and running
- New tabs appear in the current iTerm2 window
- Non-tmux sessions have limited output capture - use tmux for reliable output

## Error Handling

If the command fails:
- Check that iTerm2 is running
- Verify Python API is enabled in iTerm2 preferences
- Ensure the iTerm2 MCP server is configured correctly
- Check that the command syntax is valid

## Implementation

When invoked, this command:
1. Calls the `create_iterm_tab` MCP tool
2. Passes the command parameter (if provided)
3. Passes the profile parameter (if provided)
4. Passes the tmux_session parameter (if --tmux provided)
5. Returns the session details to the user

## See Also

- iTerm2 MCP Server documentation in plugin README
- `/shared-session` command for collaborative sessions
- `list_sessions()` tool to see all active sessions
