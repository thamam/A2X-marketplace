# Monitor Build - iTerm2 Control Skill

## Purpose
Monitor long-running build, test, or compilation processes, reporting progress and results in real-time.

## When to Use
- Running build processes (webpack, gradle, cargo, etc.)
- Executing test suites
- Running CI/CD pipelines locally
- Any long-running command that produces streaming output

## Workflow

1. **Start the Build**
   - Use `create_iterm_tab` with build command
   - Store the `session_id`
   - Announce to user that build has started

2. **Initial Check**
   - Wait 3-5 seconds for startup
   - Read initial output to confirm it started
   - Report initial status to user

3. **Periodic Monitoring**
   - Loop every 10-15 seconds:
     - Read new output (offset=0)
     - Look for progress indicators
     - Check for errors or warnings
     - Update user on significant milestones

4. **Completion Detection**
   - Check for success patterns (see below)
   - Check for failure patterns (see below)
   - Determine final status

5. **Report Results**
   - Summarize build outcome
   - Report timing if available
   - List any errors/warnings
   - Suggest next steps

6. **Cleanup**
   - Use `terminate_session` after reporting

## Success Patterns

Look for these completion indicators:
- "BUILD SUCCESSFUL"
- "✓ Build complete"
- "Compilation finished"
- "Tests passed"
- "Done in [time]"
- Exit without errors

## Failure Patterns

Look for these error indicators:
- "BUILD FAILED"
- "ERROR:"
- "FAILED"
- "✗" or "❌"
- "error:" (compilation errors)
- "Exception"
- Exit code non-zero

## Progress Indicators

Report these milestones to user:
- "Compiling..."
- "Running tests... (X/Y complete)"
- "Building modules..."
- Percentage complete if shown
- Phase changes ("Linking...", "Optimizing...")

## Example Usage

### Example 1: Frontend Build

**User Request:**
"Run the production build and let me know when it's done"

**Your Action:**

```
1. Start build:
   create_iterm_tab(command="npm run build:prod")

2. Announce:
   "Starting production build..."

3. Check after 5 seconds:
   read_session_output(session_id, offset=0, length=50)
   "Build started. Compiling 127 modules..."

4. Monitor every 10 seconds:
   Iteration 1 (10s): "Building modules: 45/127"
   Iteration 2 (20s): "Building modules: 89/127"
   Iteration 3 (30s): "Optimizing assets..."
   Iteration 4 (40s): "✓ Build complete in 38.2s"

5. Report:
   "Production build completed successfully! ✓
   - Build time: 38.2 seconds
   - Bundle size: 2.4 MB
   - No warnings or errors

   Ready for deployment!"

6. Cleanup:
   terminate_session(session_id)
```

### Example 2: Test Suite

**User Request:**
"Run the full test suite"

**Your Action:**

```
1. Start tests:
   create_iterm_tab(command="pytest tests/ -v")

2. Monitor:
   Every 10s check for progress:
   - "Running test_auth.py... 12/47 passed"
   - "Running test_api.py... 28/47 passed"
   - FAIL detected at test 31

3. Report error immediately:
   "⚠️ Test failure detected:

   FAILED tests/test_api.py::test_invalid_token
   AssertionError: Expected 401, got 200

   Should I read the full error details?"

4. If user wants details:
   read_session_output(offset=-100, length=100)
   Show relevant stack trace

5. Final report:
   "Test suite completed: 46/47 passed, 1 failed
   - Passed: 46
   - Failed: 1 (test_invalid_token)
   - Duration: 2m 14s

   The failing test is in the auth flow. Would you like me to investigate?"
```

### Example 3: Docker Build

**User Request:**
"Build the Docker image"

**Your Action:**

```
1. Start build:
   create_iterm_tab(command="docker build -t myapp:latest .")

2. Monitor phases:
   - "Step 1/8: FROM node:18" ✓
   - "Step 3/8: RUN npm install" (watching for warnings)
   - "Step 6/8: RUN npm run build" (may take longer)
   - "Step 8/8: CMD npm start" ✓

3. Report:
   "Docker image built successfully!
   - Image: myapp:latest
   - Size: 1.2 GB
   - Layers: 8
   - No security warnings

   Image ready to push or run locally."
```

## Best Practices

### Timing
- Check more frequently for fast builds (5-10s intervals)
- Check less frequently for slow builds (15-30s intervals)
- Balance responsiveness vs. spam

### User Updates
- Don't spam every check
- Report milestones and phase changes
- Always report errors immediately
- Provide percentage when available

### Error Handling
- Report errors immediately, don't wait
- Read surrounding context (±10 lines)
- Suggest potential fixes
- Offer to investigate further

### Resource Management
- Always terminate session when done
- Don't leave builds running indefinitely
- Set reasonable timeout (e.g., 10 minutes)

## Monitoring Loop Template

```python
session = create_iterm_tab(command=BUILD_COMMAND)
session_id = session["session_id"]

announce("Starting build...")

# Initial check
wait(5)
output = read_session_output(session_id, offset=0)
report_initial_status(output)

# Monitor loop
max_iterations = 60  # 10 minutes at 10s intervals
for i in range(max_iterations):
    wait(10)

    output = read_session_output(session_id, offset=0)

    if success_pattern_found(output):
        report_success(output)
        break

    if error_pattern_found(output):
        report_error(output)
        break

    if milestone_found(output):
        report_milestone(output)

terminate_session(session_id)
```

## Common Build Commands

### JavaScript/TypeScript
```bash
npm run build
npm run build:prod
npm test
npm run lint
yarn build
pnpm build
```

### Python
```bash
python setup.py build
pytest
pip install -e .
python -m build
```

### Java
```bash
mvn clean install
gradle build
./gradlew assembleRelease
```

### Rust
```bash
cargo build --release
cargo test
cargo check
```

### Docker
```bash
docker build -t name:tag .
docker-compose build
```

### Go
```bash
go build
go test ./...
go build -o binary
```

## Timeout Handling

If build exceeds reasonable time:

```
"The build is taking longer than expected (>10 minutes).
Current status: Still compiling...

Options:
1. Keep monitoring (I'll check every 30s)
2. Let it run in background (create shared session for you to check)
3. Cancel and investigate why it's slow

What would you like to do?"
```
