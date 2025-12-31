# List Terminals Command

Show all active terminal sessions managed by the iTerm2 MCP server.

## Usage

```
/list-terminals
```

## Implementation

When this command is invoked:

1. Use `list_sessions` tool
2. Format and display the results:

```
Active Terminal Sessions:
═══════════════════════════════════════════════════

Session 1:
  ID: 550e8400-e29b-41d4-a716-446655440000
  Command: npm run dev
  Control: claude
  Runtime: 2m 15s
  Lines: 342

Session 2:
  ID: 660e8400-e29b-41d4-a716-446655440001
  Command: python -i
  Control: shared
  tmux: debug-session
  Runtime: 45s
  Lines: 23

Total: 2 active sessions

Commands:
  - Read output: read_session_output(session_id)
  - Send command: send_to_session(session_id, "command")
  - Terminate: terminate_session(session_id)
  - Attach (tmux): tmux attach -t {tmux_session}
```

## Output Fields

- **ID**: Session UUID for tool calls
- **Command**: Initial command that started the session
- **Control**: Who controls the session
  - `claude`: Claude has control
  - `shared`: Both Claude and user can control (tmux)
  - `user`: User has primary control
- **tmux**: tmux session name (if applicable)
- **Runtime**: How long the session has been active
- **Lines**: Number of output lines captured

## Control Modes Explained

### `claude`
- Created with `create_iterm_tab` (no tmux)
- Claude has exclusive control
- User can see the iTerm2 tab but shouldn't type in it
- Best for: automated tasks, monitoring

### `shared`
- Created with `create_shared_session`
- Both Claude and user can control
- User can attach/detach via tmux
- Best for: debugging, collaboration

### `user`
- Session handed off to user
- User has primary control
- Claude can still observe
- Best for: manual intervention needed

## Examples

### Empty List
```
No active terminal sessions.

Create one with:
  /create-terminal [command]
  /shared-session <name> [command]
```

### Single Session
```
Active Terminal Sessions:
═══════════════════════════════════════════════════

  ID: abc-123
  Command: npm test
  Control: claude
  Runtime: 12s
  Lines: 47

Total: 1 active session
```

### Multiple Sessions
```
Active Terminal Sessions:
═══════════════════════════════════════════════════

1. npm run dev (claude) - 5m 30s - 1,245 lines
   ID: abc-123

2. python -i (shared: debug-py) - 2m 10s - 89 lines
   ID: def-456
   Attach: tmux attach -t debug-py

3. pytest tests/ (claude) - 45s - 234 lines
   ID: ghi-789

Total: 3 active sessions
```

## Notes

- Sessions are listed in creation order (oldest first)
- Session IDs are UUIDs - use the full ID for tool calls
- tmux sessions show attach command
- Runtime is calculated from session creation time
- Line count includes all captured output

## Related Commands

- `/create-terminal` - Create new session
- `/shared-session` - Create shared tmux session
- Use `terminate_session(id)` to clean up old sessions
