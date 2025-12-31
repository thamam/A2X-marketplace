# RTL (Hebrew) Support Solutions for iTerm2 and Claude Code

**Date:** 2025-12-31
**Problem:** Hebrew text displays incorrectly (left-to-right instead of right-to-left) in Claude Code when running in iTerm2 on macOS.

---

## Quick Fix for iTerm2

### Enable Experimental RTL Support

1. **Open iTerm2 Preferences** (⌘,)
2. **Navigate to:** Preferences > General > Experimental
3. **Enable:** "Enable support for right-to-left scripts"
4. **Restart iTerm2** for changes to take effect

**Location in GUI:**
```
iTerm2 > Settings > General > Experimental
├── [✓] Enable support for right-to-left scripts
└── Font compatibility: May vary
```

### Important: Text Alignment vs Character Order

**iTerm2's RTL support handles two things:**
1. ✅ **Character ordering** - Hebrew characters display right-to-left (working)
2. ❌ **Text alignment** - Text is still left-aligned (limitation)

**What this means:**
- Hebrew text will read correctly (שלום עולם displays RTL)
- But text starts from the left margin instead of right margin
- This is **expected behavior** - iTerm2 handles bidirectional text but not alignment

**Solutions for right-alignment:**
- Use the included `rtl-utils.sh` helper functions
- Use `printf` with padding for manual alignment
- See "Text Alignment Solutions" section below

---

## Text Alignment Solutions

### Quick Solution: Use rtl-utils.sh

Load the RTL utilities:
```bash
source /path/to/rtl-utils.sh
```

Available functions:
```bash
# Right-align text
rtl_print "שלום עולם"

# Right-align with custom width
rtl_printf 60 "זה טקסט בעברית"

# Center-align
center_print "שלום עולם"

# Multi-line right-aligned block
echo -e "שורה 1\nשורה 2\nשורה 3" | rtl_block
```

### Manual Alignment with printf

```bash
# Right-align to column 80
printf "%80s\n" "שלום עולם"

# Dynamic terminal width
COLS=$(tput cols)
printf "%${COLS}s\n" "שלום עולם"

# Function for easy reuse
rtl() {
    local width=$(tput cols)
    printf "%${width}s\n" "$1"
}

rtl "זה טקסט בעברית"
```

### Test Alignment

Run the alignment test script:
```bash
./test-rtl-aligned.sh
```

This will show you the difference between left-aligned (default) and right-aligned Hebrew text.

---

## Known Limitations

### iTerm2 RTL Support (v3.6.0+)

**What Works:**
- Pure Hebrew text displays RTL correctly
- Basic Unicode bidirectional algorithm support
- Works with most monospace fonts

**Known Issues:**
1. **Mixed LTR/RTL text** - English + Hebrew in same line may have ordering issues
2. **Font compatibility** - Some fonts don't render RTL properly
3. **Experimental feature** - May have bugs or incomplete behavior
4. **Terminal width calculations** - RTL text can affect cursor positioning

**Recommended Fonts for RTL:**
- Courier New
- Arial Unicode MS
- Menlo (macOS default, mixed results)
- DejaVu Sans Mono
- Liberation Mono

**Test if RTL is working:**
```bash
echo "שלום עולם"  # Should display right-to-left
echo "Hello עולם"  # Mixed text - may have issues
```

---

## Alternative Solution: VS Code RTL Extensions

If iTerm2's experimental RTL support doesn't work well, consider using Claude Code in VS Code's integrated terminal with RTL extensions.

### VS Code RTL Extensions (Published Fix)

**Option 1: RTL Text Documents Extension**
- Extension ID: `yoavbls.rtl-text-documents`
- Adds `unicode-bidi: isolate` CSS to editor
- Works in integrated terminal
- **Install:** VS Code Extensions → Search "RTL Text Documents"

**Option 2: RTL Editor Extension**
- Extension ID: `rtl-editor`
- Comprehensive RTL support for Hebrew/Arabic
- Terminal integration
- **Install:** VS Code Extensions → Search "RTL Editor"

**Option 3: RTL UI Support**
- Extension ID: `rtl-ui-support`
- System-wide RTL layout support
- Mirrors UI for RTL languages
- **Install:** VS Code Extensions → Search "RTL UI Support"

**How to enable in VS Code:**
1. Install extension from VS Code Marketplace
2. Restart VS Code
3. Open integrated terminal (Ctrl+`)
4. Hebrew text should render correctly

**VS Code Settings for RTL:**
```json
{
  "editor.unicodeBidirectional": "isolate",
  "terminal.integrated.rightClickBehavior": "default"
}
```

---

## Technical Background

### Why Terminal RTL is Hard

**Terminal Emulators (iTerm2, xterm.js):**
- Originally designed for LTR (English) text only
- Character cells are fixed-width, left-to-right
- Unicode bidirectional algorithm (UAX#9) not implemented in most terminals
- Cursor positioning assumes LTR flow

**What's Needed for RTL:**
- Unicode bidi algorithm implementation
- Font shaping and ligature support
- Reverse text flow rendering
- Mixed LTR/RTL context handling
- Cursor position calculations for RTL

### iTerm2's Approach

iTerm2 v3.6.0+ added **experimental RTL support** by:
1. Detecting RTL characters (Hebrew, Arabic scripts)
2. Reversing character order for display
3. Adjusting cursor positioning
4. Using system font rendering

**Limitations:**
- Mixed text (English + Hebrew) uses heuristics, may fail
- Complex text shaping (ligatures) not fully supported
- Performance impact on large outputs
- Not all terminal programs respect RTL (e.g., `vim`, `emacs`)

---

## Workarounds for Mixed Text Issues

If you need to display mixed English + Hebrew frequently:

### Option 1: Unicode Directional Marks
Use invisible Unicode characters to control text direction:
- `U+202E` (RIGHT-TO-LEFT OVERRIDE)
- `U+202D` (LEFT-TO-RIGHT OVERRIDE)
- `U+202C` (POP DIRECTIONAL FORMATTING)

Example:
```bash
echo -e "\u202E שלום \u202C world"
```

### Option 2: Pre-process Output
Create a shell function to wrap Hebrew text:
```bash
# Add to ~/.zshrc or ~/.bashrc
rtl() {
  echo -e "\u202E$1\u202C"
}

# Usage
rtl "שלום עולם"
```

### Option 3: Use Different Terminal

**Alternatives with better RTL support:**
- **Alacritty** - Modern GPU-accelerated terminal, has RTL patches
- **Kitty** - Has experimental RTL support
- **GNOME Terminal** (Linux) - Better RTL via VTE library
- **Windows Terminal** - Native RTL support on Windows

---

## Testing Your Setup

### Test Script
```bash
#!/bin/bash
# test-rtl.sh

echo "=== RTL Testing for Hebrew ==="
echo ""
echo "Test 1: Pure Hebrew (should be RTL)"
echo "שלום עולם"
echo ""
echo "Test 2: Mixed text (may have issues)"
echo "Hello שלום World"
echo ""
echo "Test 3: Numbers + Hebrew"
echo "123 תפוחים"
echo ""
echo "Test 4: Longer sentence"
echo "זה טקסט בעברית שצריך להיות מימין לשמאל"
echo ""
echo "Test 5: English + Hebrew + English"
echo "The word שלום means peace"
```

Save as `test-rtl.sh`, run with `bash test-rtl.sh`

**Expected behavior with RTL enabled:**
- Test 1: Displays right-to-left ✓
- Test 2: May show incorrect ordering (known issue)
- Test 3: Numbers may separate from text
- Test 4: Full RTL sentence ✓
- Test 5: Mixed ordering issues likely

---

## Recommended Solution for Claude Code

### Best Option: Enable iTerm2 Experimental RTL

**Steps:**
1. Update iTerm2 to latest version (v3.6.0+)
2. Enable experimental RTL support (Settings > General > Experimental)
3. Restart iTerm2
4. Test with Hebrew text

**If issues persist:**
1. Try different monospace fonts (Courier New, DejaVu Sans Mono)
2. Check iTerm2 version: `iTerm2 > About iTerm2`
3. Report specific issues to iTerm2 GitLab: https://gitlab.com/gnachman/iterm2/-/issues

### Fallback: Use VS Code with RTL Extension

If iTerm2's experimental support doesn't meet your needs:
1. Run Claude Code in VS Code's integrated terminal
2. Install "RTL Text Documents" extension
3. Configure VS Code settings for RTL

---

## Resources

**iTerm2 RTL Support:**
- GitLab Issue #1611: https://gitlab.com/gnachman/iterm2/-/issues/1611
- RTL Guide: https://blog.melashri.net/posts/iterm2-rtl-support/
- Experimental Features: iTerm2 > Settings > General > Experimental

**VS Code RTL:**
- RTL Text Documents Extension: https://marketplace.visualstudio.com/items?itemName=yoavbls.rtl-text-documents
- VS Code Issue #11770: RTL/bidirectional text support
- VS Code PR #269508: Bidirectional text rendering fix

**Unicode Bidirectional Algorithm:**
- UAX#9 Spec: https://unicode.org/reports/tr9/
- Bidi Test Cases: https://unicode.org/Public/UCD/latest/ucd/BidiTest.txt

---

## Summary

**Quick Fix:**
```
iTerm2 > Settings > General > Experimental > Enable RTL support
```

**Best Experience:**
- Pure Hebrew text: Works well in iTerm2 experimental mode
- Mixed LTR/RTL text: May need VS Code with RTL extension
- Heavy Hebrew usage: Consider VS Code + RTL extension

**Testing:**
Use the test script above to verify RTL is working correctly.

---

**Status:** ✅ Solution identified - iTerm2 experimental RTL support + VS Code RTL extension as fallback

---

Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>
