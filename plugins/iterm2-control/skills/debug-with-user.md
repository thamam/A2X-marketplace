# Debug with User - iTerm2 Control Skill

## Purpose
Create a collaborative debugging session where Claude sets up the environment and the user can take over for interactive debugging.

## When to Use
- Complex bugs requiring interactive debugging
- Issues where user's domain knowledge is needed
- Debugging scenarios needing real-time interaction
- When stepping through code is necessary

## Workflow

1. **Analyze the Problem**
   - Understand what needs debugging
   - Identify the relevant code/files
   - Determine debugging approach

2. **Create Shared Session**
   - Use `create_shared_session` with meaningful tmux name
   - Example: tmux_session="debug-auth-issue"
   - Optionally start relevant command (e.g., Python REPL, debugger)

3. **Set Up Debug Environment**
   - Use `send_to_session` to:
     - Import necessary modules
     - Set breakpoints
     - Navigate to problem area
     - Start debugger if needed

4. **Invite User**
   - Use `attach_user_to_session` to prepare handoff
   - Explain to user:
     - What the problem is
     - What debugging setup you've done
     - What command to run to attach
     - How to detach when done (Ctrl+B, D)

5. **User Debugs**
   - User runs: `tmux attach -t debug-auth-issue`
   - User interactively debugs
   - User detaches when done

6. **Read Results**
   - Use `read_session_output` to see what user did
   - Analyze debugging findings
   - Discuss solution with user

7. **Implement Fix**
   - Based on debugging results, implement fix
   - Or ask user for clarification

8. **Cleanup**
   - Use `terminate_session` when debugging complete

## Example Usage

**User Request:**
"There's a bug in the authentication flow. Can you help me debug it?"

**Your Action:**

```
1. Create shared session:
   create_shared_session(
     tmux_session="auth-debug",
     command="python -i"
   )

2. Set up environment:
   send_to_session("from app import auth\n")
   send_to_session("import pdb\n")
   send_to_session("auth.login('test@example.com', 'wrong_password')\n")

3. Invite user:
   "I've set up a Python debugging session with the auth module loaded.
   I tried the login with a wrong password and it's ready for debugging.

   Attach with: tmux attach -t auth-debug

   You can use pdb commands to step through the code.
   When done, press Ctrl+B then D to detach."

4. After user detaches:
   Read output to see what they found:
   read_session_output(session_id="...")

5. Discuss findings:
   "I can see from your debugging session that the password validation
   is happening before the user exists check. Should we swap those?"
```

## Best Practices

### Session Naming
- Use descriptive tmux session names
- Include the issue/feature: "bug-123-auth", "feature-search"
- Keep names short and lowercase with hyphens

### Setup Quality
- Load relevant context before handing off
- Set meaningful breakpoints
- Navigate to the problem area
- Document what you've already tried

### User Communication
- Clearly explain the problem
- Document what's already set up
- Provide clear attach command
- Explain how to detach
- Be available for questions

### After Handoff
- Wait for user to detach
- Read the complete output
- Understand what they discovered
- Ask clarifying questions if needed
- Propose solutions based on findings

## Common Debugging Scenarios

### Scenario 1: Python Code
```python
create_shared_session(tmux_session="py-debug", command="python -i")
send_to_session("import pdb\n")
send_to_session("from myapp import problematic_function\n")
send_to_session("pdb.set_trace()\n")
send_to_session("problematic_function(test_input)\n")
```

### Scenario 2: JavaScript/Node
```javascript
create_shared_session(tmux_session="node-debug", command="node inspect script.js")
```

### Scenario 3: Database Query
```sql
create_shared_session(tmux_session="db-debug", command="psql mydb")
send_to_session("\\timing on\n")
send_to_session("EXPLAIN ANALYZE SELECT...\n")
```

### Scenario 4: API Testing
```bash
create_shared_session(tmux_session="api-debug", command="bash")
send_to_session("export API_URL=http://localhost:3000\n")
send_to_session("curl -v $API_URL/api/endpoint\n")
```

## Handoff Template

Always use this template when inviting user:

```
I've created a debugging session for [PROBLEM].

Setup complete:
- [What you loaded/imported]
- [What commands you ran]
- [Current state]

To debug interactively:
  tmux attach -t [SESSION-NAME]

Tips:
- [Relevant debugging commands]
- [What to look for]
- Detach anytime: Ctrl+B then D

I'll read your session when you're done to see what you found!
```

## Troubleshooting

**User can't attach:**
- Verify tmux is installed: `which tmux`
- Check session exists: `tmux ls`
- Provide full command: `tmux attach -t session-name`

**User got disconnected:**
- They can reattach with same command
- Session persists until terminated

**Claude can't read output:**
- Verify session_id is correct
- Check session wasn't terminated
- Use offset=-50 to see last 50 lines
