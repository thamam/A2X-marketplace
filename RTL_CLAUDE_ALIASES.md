# RTL Hebrew Wrappers - Complete Command Reference

All your Claude Code/Happy aliases now have Hebrew (`-he`) versions with automatic RTL formatting!

---

## 🚀 Quick Reference

| Original Command | Hebrew RTL Version | Description |
|-----------------|-------------------|-------------|
| `happy` | `happy-he` | Default mode with RTL |
| `happy-free` | `happy-free-he` | YOLO mode with RTL |
| `claude-free` | `claude-free-he` | Same as happy-free-he |
| `happy-safe` | `happy-safe-he` | Safe mode with RTL |
| `happy-edits` | `happy-edits-he` | Auto-accept edits with RTL |
| `happy-rules` | `happy-rules-he` | Rules-only mode with RTL |
| `happy-plan` | `happy-plan-he` | Planning mode with RTL |

---

## 📦 All Available Hebrew Wrappers

### **Base Modes**
```bash
happy-he "שאלה"              # Default (asks for everything)
happy-free-he "שאלה"         # YOLO mode (no permissions)
happy-safe-he "שאלה"         # Safe mode (asks for everything)
happy-edits-he "שאלה"        # Auto-accept file edits
happy-rules-he "שאלה"        # Use settings.json rules
happy-plan-he "שאלה"         # Planning mode only
```

### **Codex Mode**
```bash
happy-codex-he "שאלה"        # Codex with permissions
happy-codex-free-he "שאלה"   # Codex YOLO mode
```

### **Gemini Mode**
```bash
happy-gemini-he "שאלה"       # Gemini with permissions
happy-gemini-free-he "שאלה"  # Gemini YOLO mode
```

### **Session Management**
```bash
happy-resume-he              # Resume session with RTL
happy-resume-free-he         # Resume YOLO with RTL
happy-continue-he            # Continue last with RTL
happy-continue-free-he       # Continue YOLO with RTL
```

### **Workflow Shortcuts**
```bash
happy-refactor-he "שאלה"     # Refactoring mode
happy-explore-he "שאלה"      # Exploration mode
happy-build-he "שאלה"        # Build mode
```

### **Claude Aliases**
```bash
claude-he "שאלה"             # Same as happy-he
claude-free-he "שאלה"        # Same as happy-free-he
he-happy "שאלה"              # Same as happy-he
he-claude "שאלה"             # Same as happy-he
```

---

## 💡 Most Common Use Cases

### **1. Quick Hebrew Query (Most Common)**
```bash
claude-free-he "מה זה TypeScript?"
```

### **2. Code Review in Hebrew**
```bash
happy-free-he "סקור את הקוד: $(cat file.ts)"
```

### **3. Refactoring with Hebrew Comments**
```bash
happy-refactor-he "שפר את הקוד עם הערות בעברית"
```

### **4. Resume Previous Hebrew Session**
```bash
happy-resume-he
```

### **5. Continue Last Session with Hebrew**
```bash
happy-continue-free-he
```

---

## 🎯 Pattern

**Every Happy/Claude alias now has a Hebrew version:**

```
Original:     <command>
Hebrew RTL:   <command>-he
```

**Examples:**
- `happy` → `happy-he`
- `happy-free` → `happy-free-he`
- `claude-free` → `claude-free-he`
- `happy-codex` → `happy-codex-he`
- `happy-resume` → `happy-resume-he`

---

## 📋 Usage Examples

### **Example 1: Using claude-free-he (Your Preferred)**
```bash
# Instead of:
claude-free "explain TypeScript"

# Use for Hebrew:
claude-free-he "הסבר TypeScript"
```

### **Example 2: Interactive Hebrew Session**
```bash
# Start session with YOLO mode + RTL
claude-free-he

# Inside session, all Hebrew output is right-aligned
> מה זה React?
> כתוב דוגמה
> תן הסבר בעברית
```

### **Example 3: Code with Hebrew Documentation**
```bash
happy-free-he "כתוב פונקציה עם תיעוד מלא בעברית"
```

### **Example 4: Resume with RTL**
```bash
# Resume your last session with RTL formatting
happy-resume-free-he
```

### **Example 5: Refactor with Hebrew**
```bash
# Refactor code with Hebrew comments
happy-refactor-he "שפר את הקוד הזה והוסף הערות בעברית"
```

---

## 🔧 Testing

Reload your shell and test:
```bash
source ~/.zshrc

# Test the wrapper
claude-free-he "שלום! זה בדיקה"
```

You should see:
- Hebrew text properly right-aligned
- Claude Code running in free/YOLO mode
- All output formatted correctly

---

## 💡 Pro Tips

### **Tip 1: Default to Hebrew for specific workflows**
```bash
# Add to ~/.zshrc if you mostly work in Hebrew:
alias refactor='happy-refactor-he'
alias review='happy-free-he'
```

### **Tip 2: Mix English and Hebrew**
```bash
# English question, Hebrew explanation
claude-free-he "Explain React hooks בעברית"
```

### **Tip 3: Pipe to clipboard**
```bash
# Get Hebrew output and copy
claude-free-he "הסבר" | tee /dev/tty | pbcopy
```

### **Tip 4: Save both versions**
```bash
# Save original and formatted
claude-free-he "שאלה" | tee original.txt | rtl_block > formatted.txt
```

---

## 🎨 Custom Shortcuts (Optional)

Add these to `~/.zshrc` for even faster access:

```bash
# Quick Hebrew shortcuts
alias cfh='claude-free-he'        # claude-free-he shorthand
alias hfh='happy-free-he'         # happy-free-he shorthand
alias he='happy-he'               # super short
alias hef='happy-free-he'         # happy-free-he short

# Workflow shortcuts
alias review-he='happy-free-he "סקור את הקוד:"'
alias doc-he='happy-free-he "כתוב תיעוד:"'
alias explain-he='happy-free-he "הסבר:"'
```

**Usage after adding:**
```bash
cfh "שאלה"                    # Super fast
review-he "$(cat file.ts)"    # Quick code review
explain-he "מושג כלשהו"       # Quick explanation
```

---

## ✅ Summary

**Your most-used command with RTL:**
```bash
claude-free-he "השאלה שלך"
```

**All your Happy/Claude aliases now have `-he` versions!**

Just add `-he` to any command you normally use, and you'll get:
- ✅ Same functionality
- ✅ Right-aligned Hebrew output
- ✅ Properly formatted RTL text

---

Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>
