---
name: collaborative-debug
description: Interactive debugging sessions with tmux for user/AI collaboration
tags: [debugging, tmux, collaboration, interactive, iterm2]
---

# Collaborative Debug

Set up collaborative debugging sessions using tmux where Claude and user can both interact with the terminal.

## Capabilities

- Create shared tmux sessions for debugging
- Set up interactive debuggers (pdb, node inspect, etc.)
- Hand off control to user for manual intervention
- Monitor user actions while they debug
- Resume collaboration after user detaches
- Guided troubleshooting workflows

## When to Use

This skill is automatically invoked when you need to:
- Debug complex issues requiring user input
- Set up interactive debugging sessions
- Allow user to take control for investigation
- Pair program with the user
- Guide users through troubleshooting
- Monitor processes while giving user access

## Usage Pattern

1. Create shared tmux session
2. Set up debugging context
3. Hand off to user with instructions
4. Monitor in background
5. User debugs and detaches
6. Analyze findings and continue

## Examples

### Python Debugging

```
User: "I need to debug the authentication flow"

Workflow:
1. create_shared_session(tmux_session="auth-debug")
2. send_to_session("cd project && source venv/bin/activate")
3. send_to_session("python -m pdb auth.py")
4. attach_user_to_session()
5. Provide instructions: "tmux attach -t auth-debug"
6. Wait for user to detach
7. read_session_output() to see findings
```

### Production Investigation

```
User: "The worker is stuck - let me investigate"

Workflow:
1. create_shared_session(tmux_session="prod-debug")
2. send_to_session("ssh prod-server")
3. send_to_session("top -p <worker-pid>")
4. attach_user_to_session()
5. User investigates
6. User detaches
7. Analyze findings
```

### Pair Programming

```
User: "Let's work on this feature together"

Workflow:
1. create_shared_session(tmux_session="pair-coding")
2. send_to_session("vim feature.ts")
3. User attaches and codes
4. Monitor changes and suggest improvements
5. Collaborative iteration
```

## User Instructions

Provide clear instructions when handing off:

```
Created shared session 'debug-session'.

To attach:
  tmux attach -t debug-session

I've set up:
  ✓ Debugger started
  ✓ Breakpoint at line 145
  ✓ Environment activated

When done:
  Detach with: Ctrl+B, then D
```

## Best Practices

- Use descriptive session names
- Set up context before handoff
- Provide clear instructions
- Monitor respectfully
- Wait for user to detach
- Analyze findings after
- Clean up when done
