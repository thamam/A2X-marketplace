# A2X Marketplace - Installation Guide

## Quick Start

### 1. Add the Marketplace

```bash
# In Claude Code
/plugin marketplace add tomerhamam/A2X-marketplace
```

### 2. Install maya-toolkit Plugin

```bash
/plugin install maya-toolkit@A2X
```

### 3. Configure Linear API (Required)

**Set environment variable:**
```bash
# Add to ~/.zshrc or ~/.bashrc
export LINEAR_API_KEY="lin_api_your_key_here"
```

Get your API key from: https://linear.app/settings/api

**Configure MCP server:**

Add to `~/.claude/config/.mcp.json`:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.linear.app/sse"],
      "env": {
        "LINEAR_API_KEY": "${LINEAR_API_KEY}"
      }
    }
  }
}
```

### 4. Restart Claude Code

```bash
# Exit and restart to load the plugin
exit
claude-code
```

## Testing the Installation

### Test 1: List Installed Plugins

```bash
/plugin list
```

**Expected output:** Should show `maya-toolkit@A2X` in the list

### Test 2: Test Task Planner

```bash
/prepare-task --help
```

**Expected output:** Task planner usage instructions

### Test 3: Test Linear Integration

```
"Get issue PRO-123"
```

**Expected output:** Linear issue details (requires valid issue ID)

### Test 4: Test Theia Walkthrough

```bash
/create-theia-inputs
```

**Expected output:** Either generates walkthrough or reports no PR changes found

### Test 5: Test Session Management

```bash
/session-handoff
```

**Expected output:** Creates `SESSION_HANDOFF.md` in current directory

## Troubleshooting

### Plugin Not Found

**Check:**
```bash
/plugin marketplace list
```

Should show `A2X` marketplace. If not:
```bash
/plugin marketplace add tomerhamam/A2X-marketplace
```

### Linear API Not Working

**Check environment variable:**
```bash
echo $LINEAR_API_KEY
```

**Test MCP server:**
```bash
npx -y mcp-remote https://mcp.linear.app/sse
```

### Commands Not Available

**Restart Claude Code:**
```bash
exit
claude-code
```

**Check plugin installation:**
```bash
/plugin list
```

## Uninstallation

### Remove Plugin

```bash
/plugin uninstall maya-toolkit
```

### Remove Marketplace

```bash
/plugin marketplace remove A2X
```

## Publishing to GitHub (For Marketplace Owner)

### 1. Push to GitHub

```bash
cd /Users/tomerhamam/personal/repos/A2X-marketplace

git add .
git commit -m "feat: add maya-toolkit plugin v1.0.0"
git push origin main
```

### 2. Update Marketplace URL

Users will then add via:
```bash
/plugin marketplace add tomerhamam/A2X-marketplace
```

### 3. Version Updates

When updating the plugin:

1. Update version in `plugins/maya-toolkit/.claude-plugin/plugin.json`
2. Update version in `.claude-plugin/marketplace.json`
3. Update version in `plugins/maya-toolkit/README.md`
4. Commit and push
5. Users run: `/plugin update maya-toolkit`

## Local Development

### Testing Plugin Changes

```bash
# Make changes to plugin files
cd /Users/tomerhamam/personal/repos/A2X-marketplace/plugins/maya-toolkit/

# Edit agents, skills, or commands
vim agents/task-planner.md

# Reinstall plugin to test
/plugin uninstall maya-toolkit
/plugin install maya-toolkit@A2X

# Or use local path for development
/plugin install /Users/tomerhamam/personal/repos/A2X-marketplace/plugins/maya-toolkit
```

### Adding New Plugins to Marketplace

1. Create plugin directory: `plugins/my-new-plugin/`
2. Add `.claude-plugin/plugin.json`
3. Add agents, skills, commands as needed
4. Create `README.md` and `SKILL.md`
5. Update `.claude-plugin/marketplace.json`:
   ```json
   "plugins": [
     {
       "name": "my-new-plugin",
       "source": "./plugins/my-new-plugin",
       "version": "1.0.0",
       "description": "Plugin description"
     }
   ]
   ```
6. Update main `README.md` with plugin info
7. Commit and push

## Best Practices

### Version Management

- Use semantic versioning: `MAJOR.MINOR.PATCH`
- Bump MAJOR for breaking changes
- Bump MINOR for new features
- Bump PATCH for bug fixes

### Documentation

- Keep `README.md` comprehensive
- Update `SKILL.md` for automatic detection patterns
- Include examples in each component
- Document all requirements

### Testing

- Test all commands locally before publishing
- Verify Linear integration works
- Test on clean Claude Code installation
- Document any environment-specific issues

## Support

**Issues:** Create issue in maya-ai repository
**Questions:** tomerhamam@gmail.com
**Marketplace:** https://github.com/tomerhamam/A2X-marketplace
