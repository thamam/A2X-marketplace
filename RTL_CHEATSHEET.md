# RTL Utilities - Quick Cheatsheet

## 🚀 Quick Start

```bash
# Open terminal (functions auto-load from ~/.zshrc)
# Just start using them!
```

---

## 📝 The 4 Main Functions

### 1️⃣ `rtl_print` - Right-align text
```bash
rtl_print "שלום עולם"
```
**Use when:** You want to print one line of Hebrew text, right-aligned.

---

### 2️⃣ `rtl_printf` - Right-align with specific width
```bash
rtl_printf 60 "זה טקסט בעברית"
```
**Use when:** You need precise control over the alignment width.

---

### 3️⃣ `center_print` - Center-align text
```bash
center_print "כותרת"
```
**Use when:** You want centered titles or headers.

---

### 4️⃣ `rtl_block` - Right-align multiple lines
```bash
echo -e "שורה 1\nשורה 2\nשורה 3" | rtl_block
```
**Use when:** You have multiple lines or file content to right-align.

---

## 💡 Common Use Cases

### Print a message
```bash
rtl_print "ההודעה שלך כאן"
```

### Display file content
```bash
cat file.txt | rtl_block
```

### Create a Hebrew header
```bash
center_print "=== כותרת ==="
```

### Multi-line text
```bash
echo -e "שורה 1\nשורה 2" | rtl_block
```

---

## 🎯 Real Example: Hebrew Script

```bash
#!/bin/bash
source ~/personal/repos/A2X-marketplace/rtl-utils.sh

center_print "תוכנית לדוגמה"
echo ""
rtl_print "מתחיל לעבוד..."
sleep 1
rtl_print "סיימתי!"
```

---

## 🔧 Optional: Create Shortcuts

Add to `~/.zshrc`:
```bash
alias he='rtl_print'
alias hec='center_print'
```

Then use:
```bash
he שלום עולם        # Instead of: rtl_print "שלום עולם"
hec כותרת           # Instead of: center_print "כותרת"
```

---

## ❓ Help

```bash
rtl_demo           # See all examples with comparisons
```

**Full guide:** `RTL_USAGE_GUIDE.md`

---

**That's it!** Just type the function name + your Hebrew text. Simple! ✨
