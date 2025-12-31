---
name: terminal
description: Create a new iTerm2 terminal tab with optional command
---

# Terminal Command

Create a new iTerm2 terminal tab with optional command execution.

## Usage

Ask Claude to create a terminal in natural language:

```
"Create a new terminal"
"Run npm test in a new terminal"
"Start the development server in a new tab"
"Create a terminal and run python server.py"
```

## What It Does

1. Creates a new iTerm2 tab in the current window
2. Optionally runs a specified command
3. Returns a session ID for further control
4. Can use specific iTerm2 profiles

## Examples

**Simple terminal:**
```
"Create a new terminal"
```

**With command:**
```
"Create a terminal and run npm test"
"Run the development server in a new tab"
```

**With profile:**
```
"Create a terminal with the Development profile and run npm start"
```

## Related

- `collaborative-debug` skill for debugging sessions
- `terminal-automation` skill for automated workflows
