# Run and Monitor - iTerm2 Control Skill

## Purpose
Execute a command in a new iTerm2 tab and monitor its output until completion or error.

## When to Use
- Running tests and checking results
- Executing build commands
- Running scripts that produce output
- Any command where you need to see the results

## Workflow

1. **Create Session**
   - Use `create_iterm_tab` tool with the command to run
   - Store the returned `session_id`

2. **Wait for Output**
   - Wait 2-3 seconds for initial output

3. **Read Output**
   - Use `read_session_output` with the `session_id`
   - Check output for completion indicators

4. **Monitor Until Complete**
   - Loop every 5 seconds:
     - Read new output (offset=0 for new lines only)
     - Check for success/failure patterns
     - Break when complete

5. **Report Results**
   - Summarize what happened
   - Show relevant output excerpts
   - Suggest next steps if errors found

6. **Cleanup**
   - Use `terminate_session` when done

## Example Usage

**User Request:**
"Run the tests and let me know if they pass"

**Your Action:**
1. Create tab: `create_iterm_tab(command="npm test")`
2. Wait 2 seconds
3. Read output and check for "PASS" or "FAIL"
4. Report: "Tests passed! ✓ All 47 tests completed successfully"
5. Terminate session

## Success Patterns
Look for these in output:
- BUILD SUCCESSFUL
- All tests passed
- Completed successfully
- ✓ or ✔ symbols
- Exit code 0

## Error Patterns
Look for these in output:
- ERROR:
- FAIL
- Exception
- exit code 1 (or non-zero)
- ✗ symbols

## Best Practices
- Always read output before terminating
- Look for completion indicators, don't guess
- Provide specific error details if found
- Offer to help fix issues discovered
- Clean up sessions after use
