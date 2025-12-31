---
name: terminal-automation
description: Automated terminal workflows using iTerm2 for testing, building, and monitoring
tags: [automation, testing, build, monitoring, iterm2]
---

# Terminal Automation

Automated terminal workflows using iTerm2 control for testing, building, monitoring, and multi-step operations.

## Capabilities

- Run test suites and analyze results
- Monitor build processes and report status
- Execute multi-step deployments
- Run commands and capture output
- Create multiple terminal sessions for different tasks
- Automate repetitive terminal operations

## When to Use

This skill is automatically invoked when you need to:
- Run tests and analyze results
- Monitor build processes
- Execute deployment scripts
- Run commands and capture output
- Setup development environments
- Monitor long-running processes

## Usage Pattern

1. Create terminal session with appropriate command
2. Wait for initial execution
3. Poll output periodically
4. Analyze results for success/failure
5. Report findings to user
6. Clean up session when complete

## Examples

### Run Tests

```
User: "Run the test suite and tell me if it passes"

Workflow:
1. create_iterm_tab(command="npm test")
2. Wait 5-10 seconds
3. read_session_output()
4. Analyze for success/failure
5. Report summary with key metrics
```

### Monitor Build

```
User: "Start the build and monitor it"

Workflow:
1. create_iterm_tab(command="npm run build")
2. Poll every 15-30 seconds
3. Look for progress indicators
4. Report status updates
5. Alert on completion or errors
```

### Setup Environment

```
User: "Set up development environment"

Workflow:
1. Create tab for server
2. Create tab for database
3. Create tab for worker
4. Monitor each for startup
5. Report ready status
```

## Best Practices

- Wait appropriately for commands to complete
- Poll efficiently (don't spam)
- Analyze output thoroughly
- Report clearly to user
- Clean up sessions when done
- Handle errors gracefully
- Set reasonable timeouts
