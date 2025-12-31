# Shared Session Command

Create a tmux session that both Claude and the user can control collaboratively.

## Usage

```
/shared-session <name> [command]
```

## Parameters

- `name` (required): tmux session name (lowercase, use hyphens)
- `command` (optional): initial command to run

## Examples

```bash
# Create debugging session
/shared-session debug-auth

# Start with Python REPL
/shared-session py-session python -i

# Create build session
/shared-session build npm run build

# Database debugging
/shared-session db-debug psql mydb
```

## Implementation

When this command is invoked:

1. Validate session name (lowercase, alphanumeric + hyphens)
2. Use `create_shared_session` tool:
   ```
   create_shared_session(
     tmux_session=name,
     command=user_command
   )
   ```
3. Provide attach instructions:
   ```
   Created shared session '{name}'! 🎯

   To attach:
     tmux attach -t {name}

   To detach:
     Press Ctrl+B, then D

   Both you and I can now control this terminal.
   I'll be able to see what you type after you detach!
   ```

## User Workflow

1. User runs: `/shared-session debug`
2. Claude creates tmux session
3. Claude provides attach command
4. User runs: `tmux attach -t debug`
5. User works interactively
6. User detaches: Ctrl+B, D
7. Claude reads what user did
8. Claude and user discuss findings

## Notes

- Requires tmux installed (`brew install tmux`)
- Sessions persist until terminated
- User can reattach multiple times
- Claude can send commands even while user attached
- Use descriptive names: `debug-auth`, `test-runner`, `build-watch`

## Best Practices

### Good Session Names
- ✓ `debug-login-bug`
- ✓ `test-runner`
- ✓ `dev-server`
- ✓ `db-queries`

### Bad Session Names
- ✗ `session1` (not descriptive)
- ✗ `DEBUG_AUTH` (uppercase)
- ✗ `debug session` (has space)
- ✗ `temp` (not meaningful)

## Common Use Cases

### Interactive Debugging
```
/shared-session debug-issue python -m pdb script.py
```

### Database Exploration
```
/shared-session db-explore psql production
```

### Log Monitoring
```
/shared-session logs tail -f /var/log/app.log
```

### Development Server
```
/shared-session dev npm run dev
```
