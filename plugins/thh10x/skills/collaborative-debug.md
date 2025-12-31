# Collaborative Debug Skill

Set up collaborative debugging sessions using tmux where Claude and user can both interact with the terminal for effective problem-solving and knowledge sharing.

## When to Use

Use this skill when you need to:
- Debug complex issues that require back-and-forth investigation
- Set up interactive debugging sessions (pdb, node inspect, etc.)
- Allow user to take control for manual intervention
- Monitor processes while giving user access
- Pair program with the user
- Train or guide users through terminal operations
- Hand off stuck processes to user for investigation

## How It Works

This skill leverages tmux integration to:

1. **Create shared tmux sessions** - Both Claude and user can connect
2. **Set up debugging context** - Prepare environment and tools
3. **Hand off control** - Let user attach and interact
4. **Monitor in background** - Claude can read output while user works
5. **Resume collaboration** - User detaches, Claude continues

## Automatic Detection

This skill is automatically invoked when users request:
- "Help me debug [issue]"
- "I need to interactively debug this"
- "Set up a debugging session I can attach to"
- "Let me take control to investigate"
- "Create a shared terminal for [task]"
- "I want to debug this myself but need setup"

## Usage Patterns

### Pattern 1: Interactive Python Debugging

```
User: "I need to debug the authentication flow"

Agent workflow:
1. Create shared tmux session: create_shared_session(tmux_session="auth-debug")
2. Send commands to set up debugging:
   - cd to correct directory
   - Set up debugger (pdb, ipdb, etc.)
   - Run the problematic code with breakpoint
3. Attach user: attach_user_to_session()
4. Inform user how to attach: "tmux attach -t auth-debug"
5. Wait for user to detach
6. Read output to see what was discovered
```

### Pattern 2: Production Issue Investigation

```
User: "The production worker is stuck - let me investigate"

Agent workflow:
1. Create shared session connecting to production
2. Set up monitoring tools (top, logs, etc.)
3. Hand off to user with context
4. User investigates interactively
5. User detaches when done
6. Claude reads session output to understand findings
7. Suggest next steps based on user's investigation
```

### Pattern 3: Pair Programming Session

```
User: "Let's work on this feature together"

Agent workflow:
1. Create shared session in project directory
2. Open relevant files in vim/editor
3. User attaches and makes changes
4. Claude monitors changes
5. Claude suggests improvements or catches issues
6. Collaborative back-and-forth
```

### Pattern 4: Guided Troubleshooting

```
User: "I'm stuck on this error"

Agent workflow:
1. Create shared session
2. Set up diagnostic commands
3. Guide user through steps: "Now run [command]"
4. User executes in shared terminal
5. Claude reads output and suggests next step
6. Iterate until issue resolved
```

## Tools Used

### Primary Tools
- `create_shared_session` - Create tmux session
- `attach_user_to_session` - Prepare for user attachment
- `send_to_session` - Send setup commands
- `read_session_output` - Monitor user's actions
- `list_sessions` - Track shared sessions

### Optional Tools
- `terminate_session` - Clean up when done
- `create_iterm_tab` - Create additional non-shared tabs if needed

## Implementation Guidelines

### Session Setup

**Create meaningful session names:**
```python
# Good names - descriptive and unique
create_shared_session(tmux_session="debug-auth-flow")
create_shared_session(tmux_session="prod-worker-stuck")
create_shared_session(tmux_session="pair-user-api")

# Avoid generic names
create_shared_session(tmux_session="debug")  # Too generic
create_shared_session(tmux_session="session1")  # Not descriptive
```

**Set up context before handing off:**
```python
# 1. Create session
result = create_shared_session(tmux_session="debug-api")
session_id = result["session_id"]

# 2. Navigate to correct location
send_to_session(session_id, "cd /path/to/project\n")

# 3. Set up environment
send_to_session(session_id, "source venv/bin/activate\n")

# 4. Prepare debugging tools
send_to_session(session_id, "export DEBUG=1\n")

# 5. Now hand off to user
attach_user_to_session(session_id)
```

### User Communication

**Clear handoff instructions:**
```markdown
"I've created a shared debugging session named 'auth-debug'.

To attach:
  tmux attach -t auth-debug

I've already:
  ✓ Navigated to the project directory
  ✓ Activated the virtual environment
  ✓ Set a breakpoint at line 145 in auth.py
  ✓ Started the application

You can now interact with the debugger. When you're done investigating,
detach with: Ctrl+B then D

I'll be monitoring in the background and can see what you discover."
```

**Guide users through tmux basics:**
```markdown
"Quick tmux guide:
  - Detach: Ctrl+B, then D
  - Scroll: Ctrl+B, then [  (arrow keys to scroll, q to exit)
  - Split pane: Ctrl+B, then %  (horizontal) or \"  (vertical)
  - Switch pane: Ctrl+B, then arrow key
  - Kill session: Ctrl+B, then :kill-session"
```

### Monitoring User Activity

**Read output periodically:**
```python
# After user attaches, check periodically
time.sleep(30)  # Give user time to work

# Read what they've done
output = read_session_output(session_id, offset=-50, length=50)

# Analyze for:
# - Commands they ran
# - Errors encountered
# - Changes made
# - Conclusions reached
```

**Respect user privacy:**
- Don't read output constantly
- Wait for user to detach before analyzing
- Ask permission before reading sensitive output

### Control Handoff

**Seamless transitions:**
```python
# Claude sets up
create_shared_session(...)
send_to_session(...)  # Setup commands

# User works
attach_user_to_session(...)
# Claude waits quietly

# User detaches
# Claude resumes
output = read_session_output(...)
# Analyze and continue
```

## Examples

### Example 1: Python Debugging Session

```markdown
User: "I need to debug why user authentication is failing"

Agent response:
"I'll set up an interactive debugging session for you."

[Creates shared tmux session: debug-auth]
[Sets up Python debugger]

"✓ Debugging session ready!

To attach:
  tmux attach -t debug-auth

I've set up:
  ✓ Virtual environment activated
  ✓ Debugger started at auth/login.py:145
  ✓ Breakpoint at the authentication check
  ✓ Test user credentials loaded

When the debugger prompts:
  - 'n' to step to next line
  - 's' to step into function
  - 'p variable_name' to print variable
  - 'c' to continue execution

Detach when done: Ctrl+B, then D"

[User debugs]
[User detaches]

[Claude reads output]

"I can see from your debugging session that the issue is in line 152 -
the password hash comparison is using the wrong salt. The expected salt
is 'user_123' but the actual salt is 'usr_123'.

Would you like me to fix the salt generation in the user creation flow?"
```

### Example 2: Production Investigation

```markdown
User: "The background worker is consuming too much memory - let me investigate"

Agent response:
"I'll set up a monitoring session connected to the production worker."

[Creates shared session]
[Sets up monitoring tools]

"✓ Production investigation session ready!

To attach:
  tmux attach -t prod-worker-monitor

I've set up:
  ✓ Connected to prod-worker-01
  ✓ top running to show memory usage
  ✓ Logs tailing in split pane: /var/log/worker.log
  ✓ Process ID: 12345

Commands available:
  - sudo kill -USR1 12345  (dump state)
  - sudo systemctl restart worker  (restart service)
  - journalctl -u worker -f  (service logs)

Detach when done: Ctrl+B, then D

⚠️ Remember: This is production. Please be careful!"

[User investigates]
[User detaches]

[Claude reads output]

"From your investigation, I can see:
  - Memory usage spiked to 4.2 GB (from normal 800 MB)
  - The spike correlates with processing job ID 789012
  - That job has a payload size of 150 MB
  - The worker is not releasing memory after processing

The issue appears to be in the job processor - it's holding references
to large payloads. Would you like me to review the garbage collection
in the job processor code?"
```

### Example 3: Pair Programming

```markdown
User: "Let's implement the WebSocket reconnection logic together"

Agent response:
"I'll set up a collaborative coding session."

[Creates shared session]

"✓ Pair programming session ready!

To attach:
  tmux attach -t pair-websocket

I've set up:
  ✓ Opened frontend/src/websocket.ts in vim
  ✓ Tests running in watch mode (split pane)
  ✓ Browser with DevTools at http://localhost:3000

You can edit the code directly. I'll monitor the test results and
suggest improvements.

Detach when done: Ctrl+B, then D"

[User codes]
[Claude monitors tests]

[Claude sees test failure]

"I notice the test 'should reconnect after disconnect' is failing.
The error is: 'Expected 1 reconnection attempt, got 0'

Looking at line 45, I think the issue is that the reconnect timer
isn't being set. Try adding:

  this.reconnectTimer = setTimeout(() => this.connect(), delay)

after line 43."

[User makes change]
[Tests pass]

"✅ Tests are passing now! Great work. The reconnection logic looks solid."
```

## Edge Cases

### User Doesn't Have tmux

If user doesn't have tmux:
```markdown
"To use shared debugging sessions, you need tmux installed.

Install with:
  brew install tmux    # macOS
  sudo apt install tmux  # Linux

Alternatively, I can run the debugging commands in a regular terminal
and report the output to you. Would you prefer that?"
```

### Session Name Conflict

If tmux session already exists:
```python
# Handle gracefully
try:
    create_shared_session(tmux_session="debug")
except SessionExistsError:
    # Suggest different name or reuse
    create_shared_session(tmux_session="debug-2")
```

### User Gets Stuck in tmux

Provide escape hatch:
```markdown
"If you're stuck in the tmux session:
  - Detach: Ctrl+B, then D
  - Force quit: Ctrl+B, then :kill-session
  - Or just close the terminal window

I can recreate the session if needed."
```

## Best Practices

### ✅ Do This

- **Set up context first** - Navigate, activate, prepare
- **Use descriptive names** - Easy to find and remember
- **Provide clear instructions** - How to attach, navigate, detach
- **Guide users** - Explain what's set up and why
- **Monitor respectfully** - Don't intrude, wait for detach
- **Analyze findings** - Learn from user's investigation
- **Clean up** - Terminate sessions when done

### ❌ Avoid This

- **Don't leave setup to user** - Prepare the environment
- **Don't use generic names** - Be specific and descriptive
- **Don't assume tmux knowledge** - Provide basics
- **Don't read output constantly** - Respect privacy
- **Don't interfere while user works** - Wait for detach
- **Don't leave zombie sessions** - Clean up resources

## Integration with Other Skills

This skill works well with:
- **terminal-automation** - Can hand off to user if automation gets stuck
- **monitoring skills** - Set up monitoring, let user investigate
- **development skills** - Pair programming and collaborative coding

## Version History

- **v1.0.0** - Initial release
  - tmux-based shared sessions
  - Interactive debugging support
  - User handoff and resume
  - Guided troubleshooting
