---
name: shared-session
description: Create a shared tmux session for collaboration
---

# Shared Session Command

Create a shared tmux session for collaboration between Claude and user.

## Usage

Ask Claude to create a shared session in natural language:

```
"Create a shared debugging session"
"Set up a tmux session I can attach to"
"Create a collaborative terminal for debugging"
"Create a shared session called 'dev-work'"
```

## What It Does

1. Creates a new tmux session with the given name
2. Creates an iTerm2 tab attached to that session
3. Optionally runs an initial command
4. Provides attachment instructions for the user
5. Enables bidirectional control (Claude + user)

## Examples

**Simple shared session:**
```
"Create a shared debugging session"
```

**With specific name:**
```
"Create a shared session called 'api-debug'"
```

**With command:**
```
"Create a shared session and run python debug.py"
```

## User Attachment

After creating, user can attach with:
```bash
tmux attach -t session-name
```

User can detach with:
```
Ctrl+B, then D
```

## Related

- `collaborative-debug` skill for debugging workflows
- `terminal-automation` skill for automated tasks
