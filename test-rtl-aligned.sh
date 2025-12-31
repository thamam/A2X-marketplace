#!/bin/bash
# RTL Testing Script with Right Alignment
# Demonstrates right-aligned Hebrew text

# Get terminal width
COLS=$(tput cols)

# Function to right-align text
right_align() {
    local text="$1"
    local length=${#text}
    local padding=$((COLS - length))
    printf "%${padding}s%s\n" "" "$text"
}

echo "=== RTL Testing with Right Alignment ==="
echo ""

echo "Test 1: Pure Hebrew (LEFT-aligned - default)"
echo "שלום עולם"
echo ""

echo "Test 1b: Pure Hebrew (RIGHT-aligned)"
right_align "שלום עולם"
echo ""

echo "Test 2: Mixed text (LEFT-aligned)"
echo "Hello שלום World"
echo ""

echo "Test 2b: Mixed text (RIGHT-aligned)"
right_align "Hello שלום World"
echo ""

echo "Test 4: Longer sentence (LEFT-aligned)"
echo "זה טקסט בעברית שצריך להיות מימין לשמאל"
echo ""

echo "Test 4b: Longer sentence (RIGHT-aligned)"
right_align "זה טקסט בעברית שצריך להיות מימין לשמאל"
echo ""

echo "=== Using printf for precise alignment ==="
printf "%80s\n" "שלום עולם"
printf "%80s\n" "זה משפט ארוך יותר בעברית"
