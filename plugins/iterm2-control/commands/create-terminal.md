# Create Terminal Command

Create a new iTerm2 terminal session with an optional command.

## Usage

```
/create-terminal [command]
```

## Examples

```bash
# Create empty terminal
/create-terminal

# Create and run command
/create-terminal npm start

# Run Python REPL
/create-terminal python -i

# Start development server
/create-terminal npm run dev
```

## Implementation

When this command is invoked:

1. Extract the command from arguments (if provided)
2. Use `create_iterm_tab` tool:
   ```
   create_iterm_tab(command=user_command)
   ```
3. Report the session_id to user:
   ```
   Created new terminal session!
   Session ID: {session_id}

   You can now:
   - Send commands with: /send-command {session_id} {command}
   - Read output with: read_session_output
   - Terminate with: terminate_session
   ```

## Notes

- Store the session_id for future reference
- The terminal tab will open in iTerm2
- Session remains active until terminated
- Can create multiple sessions concurrently
