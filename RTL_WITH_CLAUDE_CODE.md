# Using RTL Utilities with Claude Code Sessions

## 🎯 Overview

You have **3 ways** to use RTL utilities with Claude Code:

1. **Wrapper functions** - Run Claude with auto RTL formatting
2. **Pipe output** - Format Claude's output after it runs
3. **During session** - Use RTL functions while Claude Code is active

---

## Method 1: Wrapper Functions (Easiest)

### **New aliases added to your shell:**

```bash
happy-he "שאלה בעברית"      # Happy with RTL output
claude-he "שאלה בעברית"     # Same thing (alias)
```

**What it does:**
- Runs Claude Code normally
- Automatically right-aligns all Hebrew output
- Works for any Hebrew conversation

**Example:**
```bash
happy-he "הסבר לי מה זה TypeScript"
# All Hebrew responses will be right-aligned
```

---

## Method 2: Pipe Output

### **Manual piping for specific cases:**

```bash
# Regular Claude output → right-aligned
happy "שאלה" | rtl_block

# Save to file and display right-aligned
happy "שאלה" | tee output.txt | rtl_block

# Only show right-aligned, don't save
happy "שאלה" 2>&1 | rtl_block
```

**When to use:**
- You want control over when to apply RTL
- You're processing output further
- You want to save original + formatted versions

---

## Method 3: During Active Session

### **Using RTL functions while Claude Code is running:**

When you're already in a Claude Code session:

```bash
# 1. Start normal Claude session
happy

# 2. Inside the session, Claude might output Hebrew text
# The text appears left-aligned

# 3. Exit session (Ctrl+D or type /exit)

# 4. In your next command, use the wrapper:
happy-he

# Or manually format previous output:
cat ~/.claude-code/logs/last-session.txt | rtl_block
```

### **For scripting with Claude:**

```bash
#!/bin/bash
source ~/personal/repos/A2X-marketplace/rtl-utils.sh

# Print Hebrew prompt
rtl_print "מריץ Claude Code..."

# Run Claude with Hebrew query
happy-he "כתוב לי פונקציה בעברית"

# Print Hebrew completion message
rtl_print "הסתיים!"
```

---

## Method 4: Claude Code Slash Commands (Advanced)

### **Create a custom slash command for RTL output:**

Create: `~/.claude-code/commands/he.md`
```markdown
Run the following user query and format any Hebrew output with right-alignment.

Use the rtl_print function for single lines and rtl_block for multi-line Hebrew text.

User query: {{query}}
```

**Usage:**
```bash
happy
> /he מה זה TypeScript
```

---

## Real-World Examples

### **Example 1: Code Review in Hebrew**
```bash
happy-he "סקור את הקוד הזה ותן המלצות בעברית: $(cat file.ts)"
```

### **Example 2: Documentation in Hebrew**
```bash
happy-he "כתוב תיעוד בעברית לפונקציה הזו"
```

### **Example 3: Error Explanation in Hebrew**
```bash
# Copy error message, then:
happy-he "הסבר את השגיאה הזו בעברית: $(pbpaste)"
```

### **Example 4: Interactive Session with Hebrew**
```bash
# Start Hebrew-friendly session
happy-he

# Inside session, all Hebrew responses are right-aligned
> מה זה React hooks?
> הסבר על useState
> תן דוגמה בעברית
```

### **Example 5: Hebrew Code Comments**
```bash
# Generate code with Hebrew comments
happy-he "כתוב פונקציה עם הערות בעברית"
```

---

## Formatting Claude's Existing Output

### **If Claude already output Hebrew text (left-aligned):**

**Option A: Re-run with wrapper**
```bash
# Instead of: happy "שאלה"
# Use:
happy-he "שאלה"
```

**Option B: Format saved output**
```bash
# If you saved the output
cat output.txt | rtl_block

# Or format specific lines
grep "שלום" output.txt | rtl_block
```

**Option C: Format clipboard**
```bash
# Copy Claude's Hebrew output, then:
pbpaste | rtl_block
```

---

## Combining with Other Tools

### **With grep:**
```bash
happy-he "שאלה" | grep "מילה" | rtl_block
```

### **With less:**
```bash
happy-he "שאלה ארוכה" | less
# Hebrew text will be right-aligned in pager
```

### **With file save:**
```bash
# Save original (left-aligned)
happy "שאלה" > original.txt

# Save formatted (right-aligned)
happy "שאלה" | rtl_block > formatted.txt

# Or both
happy "שאלה" | tee original.txt | rtl_block > formatted.txt
```

---

## Tips & Tricks

### **Tip 1: Default to Hebrew mode**
```bash
# Add to ~/.zshrc if you mostly work in Hebrew:
alias happy='happy-he'
```

### **Tip 2: Quick Hebrew print**
```bash
# During any session, you can use:
rtl_print "הודעה מהירה בעברית"
```

### **Tip 3: Format clipboard Hebrew**
```bash
# Copy text, then:
pbpaste | rtl_block | pbcopy
# Now paste - it's right-aligned!
```

### **Tip 4: Hebrew logging**
```bash
# In your scripts:
log_he() {
    echo "[$(date)] $*" | rtl_block
}

log_he "הפעולה הסתיימה בהצלחה"
```

---

## Quick Reference

| What you want | Command |
|--------------|---------|
| Claude with RTL output | `happy-he "שאלה"` |
| Pipe to RTL | `happy "שאלה" \| rtl_block` |
| Print Hebrew message | `rtl_print "הודעה"` |
| Format file content | `cat file.txt \| rtl_block` |
| Format clipboard | `pbpaste \| rtl_block` |
| Hebrew menu | See examples above |

---

## Troubleshooting

### **Hebrew text still left-aligned?**

**Check iTerm2 RTL support:**
```bash
# iTerm2 > Settings > General > Experimental
# Enable "Enable support for right-to-left scripts"
```

**Reload shell:**
```bash
source ~/.zshrc
```

**Test utilities:**
```bash
rtl_print "שלום"
# Should be right-aligned
```

### **Functions not found?**

```bash
# Check if loaded
type rtl_print

# If not found, manually load:
source ~/personal/repos/A2X-marketplace/rtl-utils.sh
```

### **Claude output not formatting?**

**Make sure you're using the wrapper:**
```bash
# Wrong: happy "שאלה"
# Right: happy-he "שאלה"
```

---

## Summary

✅ **Easiest way:**
```bash
happy-he "שאלה בעברית"
```

✅ **During session:**
Use `rtl_print` and `rtl_block` functions

✅ **Format existing output:**
```bash
cat output.txt | rtl_block
```

**That's it!** Your Claude Code sessions now support proper RTL Hebrew formatting. 🎉

---

Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>
