#!/bin/bash
# Demo: Hebrew output with Claude Code

source ~/personal/repos/A2X-marketplace/rtl-utils.sh

echo "=== Demo: Hebrew Output Formatting ==="
echo ""

echo "1. Regular echo (left-aligned):"
echo "שלום! זה דוגמה לטקסט בעברית"
echo ""

echo "2. Using rtl_print (right-aligned):"
rtl_print "שלום! זה דוגמה לטקסט בעברית"
echo ""

echo "3. Simulated Claude Code output (left-aligned):"
cat << EOF
התשובה לשאלה שלך:
TypeScript הוא שפת תכנות
שמוסיפה טיפוסים ל-JavaScript
EOF
echo ""

echo "4. Same output with rtl_block (right-aligned):"
cat << EOF | rtl_block
התשובה לשאלה שלך:
TypeScript הוא שפת תכנות
שמוסיפה טיפוסים ל-JavaScript
EOF
echo ""

echo "=== To use with real Claude Code: ==="
rtl_print "happy-he \"השאלה שלך בעברית\""
