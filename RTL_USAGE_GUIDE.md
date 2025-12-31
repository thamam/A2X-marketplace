# RTL Utilities - Usage Guide

## Quick Start

### 1. Reload Your Shell (one time)
```bash
source ~/.zshrc
```

Or just open a new terminal window - the utilities load automatically.

---

## Available Functions

### `rtl_print` - Right-align text

**Basic usage:**
```bash
rtl_print "שלום עולם"
```

**Output:**
```
                                                                       שלום עולם
```

**With custom width:**
```bash
rtl_print "שלום עולם" 50
```

**Output:**
```
                                   שלום עולם
```

---

### `rtl_printf` - Right-align with specific width

**Usage:**
```bash
rtl_printf 60 "זה טקסט בעברית"
```

**Output:**
```
                                  זה טקסט בעברית
```

**Multiple words:**
```bash
rtl_printf 70 "שלום עולם זה משפט ארוך יותר"
```

---

### `center_print` - Center-align text

**Basic usage:**
```bash
center_print "שלום עולם"
```

**Output:**
```
                                   שלום עולם
```

**With custom width:**
```bash
center_print "כותרת" 80
```

---

### `rtl_block` - Right-align multiple lines

**Usage with echo:**
```bash
echo -e "שורה ראשונה\nשורה שנייה\nשורה שלישית" | rtl_block
```

**Output:**
```
                                                                  שורה ראשונה
                                                                   שורה שנייה
                                                                  שורה שלישית
```

**Usage with heredoc:**
```bash
cat << EOF | rtl_block
זוהי שורה ראשונה
זוהי שורה שנייה
זוהי שורה שלישית
EOF
```

**Usage with file:**
```bash
cat hebrew-file.txt | rtl_block
```

---

### `rtl_demo` - See all examples

**Usage:**
```bash
rtl_demo
```

This shows side-by-side comparisons of left-aligned vs right-aligned text.

---

## Practical Examples

### Example 1: Print a Hebrew greeting
```bash
rtl_print "שלום! איך אתה?"
```

### Example 2: Create a Hebrew menu
```bash
echo "=== תפריט ראשי ===" | rtl_block
echo ""
rtl_print "1. אפשרות ראשונה"
rtl_print "2. אפשרות שנייה"
rtl_print "3. אפשרות שלישית"
```

### Example 3: Hebrew headers in scripts
```bash
#!/bin/bash
center_print "=== סקריפט לדוגמה ==="
echo ""
rtl_print "התחלת הסקריפט..."
# Your commands here
rtl_print "הסקריפט הסתיים בהצלחה"
```

### Example 4: Display Hebrew file content
```bash
# Right-align every line of a Hebrew file
cat document.txt | rtl_block
```

### Example 5: Create a function for Hebrew echo
```bash
# Add to your .zshrc for convenience
he() {
    rtl_print "$*"
}

# Usage:
he שלום עולם
he זה קל יותר
```

---

## Integration with Scripts

### In a bash/zsh script:
```bash
#!/bin/bash

# Source RTL utilities
source ~/personal/repos/A2X-marketplace/rtl-utils.sh

# Now use them
rtl_print "=== הודעת התחלה ==="
echo ""

# Your script logic here
echo "Running commands..."

rtl_print "=== הודעת סיום ==="
```

---

## Combining with Regular Output

### Mixed English and Hebrew:
```bash
echo "Status:"
rtl_print "הכל עובד כשורה"
echo ""
echo "Details:"
rtl_print "הפעולה הושלמה בהצלחה"
```

### Creating formatted output:
```bash
echo "╔════════════════════════════════════════╗"
center_print "כותרת מרכזית"
echo "╚════════════════════════════════════════╝"
rtl_print "תוכן הטקסט כאן"
```

---

## Helper Aliases (Optional)

Add these to your `~/.zshrc` for even easier usage:

```bash
# Hebrew echo - right-aligned
alias he='rtl_print'

# Hebrew cat - right-align file content
alias hecat='rtl_block < '

# Hebrew center
alias hec='center_print'
```

**Usage after adding aliases:**
```bash
he שלום עולם              # Instead of: rtl_print "שלום עולם"
hecat file.txt           # Instead of: cat file.txt | rtl_block
hec כותרת                 # Instead of: center_print "כותרת"
```

---

## Troubleshooting

### Functions not found?
```bash
# Reload your shell
source ~/.zshrc

# Or verify the file exists
ls -l ~/personal/repos/A2X-marketplace/rtl-utils.sh

# Or manually source it
source ~/personal/repos/A2X-marketplace/rtl-utils.sh
```

### Text still left-aligned?
Make sure iTerm2's RTL support is enabled:
- iTerm2 > Settings > General > Experimental
- Enable "Enable support for right-to-left scripts"
- Restart iTerm2

### Character order still wrong?
The functions only handle alignment, not character order.
Character order is handled by iTerm2's RTL support (see above).

---

## Summary

**Quick reference:**
```bash
rtl_print "text"              # Right-align single line
rtl_printf 60 "text"          # Right-align with width
center_print "text"           # Center-align
echo "text" | rtl_block       # Right-align multiple lines
rtl_demo                      # See all examples
```

**Workflow:**
1. Open terminal (functions auto-load)
2. Type `rtl_print "שלום עולם"`
3. Press Enter
4. See right-aligned Hebrew text!

---

Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>
