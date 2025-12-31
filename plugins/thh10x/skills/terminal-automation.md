# Terminal Automation Skill

Automated terminal workflows using iTerm2 control for testing, building, monitoring, and multi-step operations.

## When to Use

Use this skill when you need to:
- Run test suites and analyze results automatically
- Monitor build processes and report status
- Execute multi-step deployment or setup workflows
- Run commands and capture output for analysis
- Create multiple terminal sessions for different tasks
- Automate repetitive terminal operations

## How It Works

This skill leverages the iTerm2 MCP server to:

1. **Create terminal sessions** - Spawn new iTerm2 tabs with specific commands
2. **Execute commands** - Send text and commands to running sessions
3. **Monitor output** - Read and analyze terminal output with pagination
4. **Track multiple sessions** - Manage concurrent terminal operations
5. **Report results** - Analyze output and report back to user

## Automatic Detection

This skill is automatically invoked when users request:
- "Run the tests and let me know if they pass"
- "Start the build and monitor it"
- "Execute the deployment script and check for errors"
- "Run [command] and show me the output"
- "Set up multiple terminals for [project]"
- "Monitor [process] until it completes"

## Usage Patterns

### Pattern 1: Run Tests and Report Results

```
User: "Run the test suite and tell me if it passes"

Agent workflow:
1. Use create_iterm_tab(command="npm test") to start tests
2. Wait a reasonable time for completion (e.g., 5-10 seconds)
3. Use read_session_output() to get the results
4. Analyze output for success/failure indicators
5. Report summary to user with key metrics
6. Optionally terminate_session() when done
```

### Pattern 2: Monitor Long-Running Build

```
User: "Start the production build and monitor it"

Agent workflow:
1. Use create_iterm_tab(command="npm run build:prod")
2. Periodically poll with read_session_output()
3. Look for progress indicators
4. Report status updates to user
5. Alert on completion or errors
6. Provide build summary (time, size, warnings)
```

### Pattern 3: Multi-Step Deployment

```
User: "Deploy to staging - run migrations, build, and deploy"

Agent workflow:
1. Create session for database migrations
2. Monitor until migrations complete
3. Create session for build process
4. Monitor until build completes
5. Create session for deployment
6. Monitor until deployment completes
7. Report overall success/failure with details
```

### Pattern 4: Development Environment Setup

```
User: "Set up development environment with server, database, and worker"

Agent workflow:
1. Create tab for server: create_iterm_tab(command="npm run dev")
2. Create tab for database: create_iterm_tab(command="docker-compose up db")
3. Create tab for worker: create_iterm_tab(command="npm run worker")
4. Monitor each for successful startup
5. Report which services are running
6. Keep sessions open for user
```

## Tools Used

### Primary Tools
- `create_iterm_tab` - Create new terminal sessions
- `read_session_output` - Read terminal output
- `send_to_session` - Send additional commands if needed
- `list_sessions` - Track active sessions
- `terminate_session` - Clean up when done

### Optional Tools
- `create_shared_session` - For long-running processes user may want to monitor
- `attach_user_to_session` - Hand off control if issues arise

## Implementation Guidelines

### Timing and Polling

**Initial wait times:**
- Quick commands (ls, git status): 1-2 seconds
- Test suites: 5-10 seconds initial, then poll
- Build processes: 10-15 seconds initial, then poll every 10-30s
- Deployments: 15-30 seconds initial, then poll every 30-60s

**Polling strategy:**
```python
# Don't poll too frequently - be efficient
initial_wait = 10  # seconds
poll_interval = 15  # seconds
max_polls = 20     # stop after ~5 minutes

time.sleep(initial_wait)
for i in range(max_polls):
    output = read_session_output(session_id)
    if is_complete(output):
        break
    time.sleep(poll_interval)
```

### Output Analysis

Look for common completion indicators:

**Success indicators:**
- "All tests passed"
- "BUILD SUCCESSFUL"
- "Deployment complete"
- "✓" or "✔" characters
- Exit codes (if visible)

**Failure indicators:**
- "FAILED", "ERROR", "FATAL"
- "✗" or "✖" characters
- Stack traces
- "Error:" prefix

**Progress indicators:**
- Percentage complete (75%)
- Step counters (3/10)
- Time elapsed
- Current operation name

### Resource Management

**Always clean up:**
- Terminate sessions when complete
- Don't leave orphaned processes
- Close tabs that are no longer needed

**Track sessions:**
- Store session_id for each operation
- Use meaningful names in logs
- Report active sessions to user

## Examples

### Example 1: Test Suite Analysis

```markdown
User: "Run the Jest tests and analyze the results"

Agent response:
"I'll run the test suite and analyze the results."

[Creates terminal with: npm test]
[Waits 8 seconds]
[Reads output]

"✅ Test suite completed successfully!

Results:
- Total tests: 127
- Passed: 125 (98.4%)
- Failed: 2
- Skipped: 0
- Duration: 6.2 seconds

Failed tests:
1. auth.test.ts:45 - "should validate expired tokens"
2. api.test.ts:112 - "should handle rate limiting"

Would you like me to show the full output for the failed tests?"
```

### Example 2: Build Monitoring

```markdown
User: "Start the production build and monitor it"

Agent response:
"I'll start the production build and monitor progress."

[Creates terminal with: npm run build:prod]
[Polls every 15 seconds]

[After 30s]
"⏳ Build in progress (30s elapsed):
  ✓ TypeScript compilation complete
  ✓ Assets bundled
  ⏳ Running optimizations..."

[After 2m 15s]
"✅ Build completed successfully!

Summary:
- Total time: 2m 15s
- Bundle size: 2.4 MB (gzipped: 842 KB)
- Output directory: dist/
- Warnings: 0
- Errors: 0

The build artifacts are ready for deployment."
```

### Example 3: Environment Setup

```markdown
User: "Set up local development environment"

Agent response:
"I'll set up the development environment with all required services."

[Creates 3 terminals]
1. Server: npm run dev
2. Database: docker-compose up postgres
3. Redis: docker-compose up redis

[Monitors all sessions]

"✅ Development environment is ready!

Services running:
✓ Web server - http://localhost:3000
✓ Database - localhost:5432
✓ Redis - localhost:6379

All services started successfully. You can now begin development!"
```

## Edge Cases

### Handle Long-Running Processes

Don't block forever - set reasonable timeouts:

```python
max_runtime = 600  # 10 minutes max
start_time = time.time()

while time.time() - start_time < max_runtime:
    output = read_session_output(session_id)
    if is_complete(output):
        break
    time.sleep(poll_interval)
else:
    # Timeout reached
    report_timeout_to_user()
```

### Handle Failed Commands

Check for errors early:

```python
# Wait briefly
time.sleep(2)
output = read_session_output(session_id)

# Check for immediate failures
if "command not found" in output["output"] or \
   "No such file" in output["output"]:
    report_error_immediately()
    return
```

### Handle Interactive Prompts

If a command requires user input:

```python
output = read_session_output(session_id)
if "Press Y to continue" in output["output"] or \
   "Enter password" in output["output"]:
    # Hand off to user
    create_shared_session_if_needed()
    tell_user_input_required()
```

## Best Practices

### ✅ Do This

- **Wait appropriately** - Give commands time to complete
- **Poll efficiently** - Don't spam read_session_output
- **Analyze thoroughly** - Look for success/failure indicators
- **Report clearly** - Summarize results for user
- **Clean up** - Terminate sessions when done
- **Handle errors** - Check for failures early
- **Set timeouts** - Don't wait forever

### ❌ Avoid This

- **Don't poll too fast** - Wastes resources
- **Don't assume success** - Always check output
- **Don't leave sessions** - Clean up when done
- **Don't ignore errors** - Report failures immediately
- **Don't block indefinitely** - Set reasonable timeouts

## Integration with Other Skills

This skill works well with:
- **collaborative-debug** - Hand off when issues need investigation
- **session management** - For long-running processes

## Version History

- **v1.0.0** - Initial release
  - Automated test execution
  - Build monitoring
  - Multi-step workflows
  - Session management
