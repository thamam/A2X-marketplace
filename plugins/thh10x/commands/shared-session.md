# /shared-session

Create a shared tmux session for collaboration between Claude and user.

## Usage

```bash
/shared-session debug                     # Create session named "debug"
/shared-session dev-work                  # Create session named "dev-work"
/shared-session monitoring tail -f app.log  # Session with command
```

## Description

This command creates a persistent tmux session that both Claude and the user can interact with. The user can attach to the session to take control, work interactively, and detach when done. Claude can monitor the session and read output in the background.

This is ideal for collaborative debugging, pair programming, and situations where you want to hand off control to the user while maintaining context.

## Parameters

- **session-name** (required): Unique name for the tmux session
- **command** (optional): Initial command to run in the session

## Examples

### Basic Usage

```bash
# Create empty session for general work
/shared-session dev-work

# Create debugging session
/shared-session debug-auth

# Create session with running server
/shared-session server npm run dev

# Create monitoring session
/shared-session logs tail -f /var/log/app.log
```

### Advanced Usage

```bash
# Production investigation
/shared-session prod-debug ssh prod-server

# Database session
/shared-session db-client psql -U postgres

# Build monitoring
/shared-session build-watch npm run build:watch
```

## When to Use

Use this command when you need to:
- Debug issues interactively with user input
- Hand off control for manual intervention
- Create persistent sessions that survive disconnections
- Share terminal access between Claude and user
- Monitor long-running processes while allowing user access
- Pair program with the user
- Set up collaborative troubleshooting sessions

## Output

The command will:
1. Create a new tmux session with the given name
2. Create a new iTerm2 tab attached to that session
3. Run the initial command (if provided)
4. Show the `tmux attach` command for the user
5. Return session details including session_id

## User Instructions

After creating a shared session, the user can:

**Attach to session:**
```bash
tmux attach -t session-name
```

**Detach from session:**
- Press `Ctrl+B`, then press `D`
- Or just close the terminal window

**Check if session exists:**
```bash
tmux ls
```

**Kill session when done:**
```bash
tmux kill-session -t session-name
```

## Related

- `/create-terminal` - Create a regular (non-shared) terminal
- `collaborative-debug` skill - For interactive debugging workflows
- `attach_user_to_session` tool - Prepare existing session for user attachment

## Notes

- **Requires tmux** - Install with `brew install tmux` (macOS) or `sudo apt install tmux` (Linux)
- **Persistent** - Sessions survive terminal disconnections
- **Shared control** - Both Claude and user can send commands
- **Full output capture** - tmux sessions have reliable output buffering
- **Multiple attachments** - Multiple users can attach to same session

## Workflow Example

```markdown
User: "I need to debug the API authentication"

Claude: "I'll create a shared debugging session."

[Runs: /shared-session debug-auth python -m pdb api/auth.py]

Claude: "Created shared session 'debug-auth'.

To attach:
  tmux attach -t debug-auth

I've started the Python debugger. You can now:
  - Set breakpoints with 'b <line>'
  - Step through with 'n' (next) or 's' (step into)
  - Print variables with 'p <variable>'

When done, detach with: Ctrl+B, then D"

[User attaches, debugs, detaches]

[Claude reads session output]

Claude: "I can see from your debugging session that the issue
is in the token validation logic at line 145..."
```

## Control Modes

Shared sessions operate in **shared mode**, meaning:
- Both Claude and user can send commands
- Claude warns before sending commands while user is attached
- User has priority - Claude waits if user is typing
- Output is visible to both Claude and user

## Best Practices

### ✅ Do This

- **Use descriptive names** - "debug-auth" not "session1"
- **Set up context first** - Navigate to correct directory, activate environment
- **Provide user instructions** - Tell them how to attach and detach
- **Clean up when done** - Terminate sessions you no longer need
- **Wait for user to detach** - Don't interfere while they're working

### ❌ Avoid This

- **Don't use generic names** - Makes sessions hard to identify
- **Don't create without purpose** - Have a clear reason for the session
- **Don't spam commands** - Wait between sending commands
- **Don't leave zombie sessions** - Clean up after use

## Troubleshooting

### "tmux: command not found"

Install tmux:
```bash
# macOS
brew install tmux

# Linux
sudo apt install tmux
```

### "session already exists"

The session name is already in use. Either:
- Choose a different name
- Kill the existing session: `tmux kill-session -t session-name`
- Attach to the existing session instead

### "no sessions"

When running `tmux ls`, no sessions found means:
- No tmux sessions are currently running
- Create one with `/shared-session`

## Error Handling

If the command fails:
- Check that tmux is installed (`which tmux`)
- Verify the session name is valid (alphanumeric, dashes, underscores)
- Ensure iTerm2 is running with Python API enabled
- Check that the iTerm2 MCP server is configured

## Implementation

When invoked, this command:
1. Calls the `create_shared_session` MCP tool
2. Passes the session name and optional command
3. Creates a new iTerm2 tab attached to the tmux session
4. Returns attachment instructions and session details
5. Stores session_id for later reference

## See Also

- iTerm2 MCP Server documentation in plugin README
- tmux documentation: `man tmux` or https://github.com/tmux/tmux/wiki
- `collaborative-debug` skill for debugging workflows
- `terminal-automation` skill for automated workflows
