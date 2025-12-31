#!/bin/bash
# RTL Utilities for Terminal Output
# Source this file: source rtl-utils.sh

# Get terminal width
get_terminal_width() {
    tput cols 2>/dev/null || echo 80
}

# Right-align text
rtl_print() {
    local text="$1"
    local width="${2:-$(get_terminal_width)}"
    local length=${#text}
    local padding=$((width - length))
    printf "%${padding}s%s\n" "" "$text"
}

# Right-align with custom width
rtl_printf() {
    local width="$1"
    shift
    printf "%${width}s\n" "$*"
}

# Center-align (useful for titles)
center_print() {
    local text="$1"
    local width="${2:-$(get_terminal_width)}"
    local length=${#text}
    local padding=$(((width - length) / 2))
    printf "%${padding}s%s\n" "" "$text"
}

# Print RTL text block (multiple lines)
rtl_block() {
    while IFS= read -r line; do
        rtl_print "$line"
    done
}

# Example usage function (run manually with: rtl_demo)
rtl_demo() {
    echo "=== RTL Utilities Demo ==="
    echo ""
    echo "Regular echo (left-aligned):"
    echo "שלום עולם"
    echo ""
    echo "rtl_print (right-aligned):"
    rtl_print "שלום עולם"
    echo ""
    echo "rtl_printf with custom width:"
    rtl_printf 60 "זה טקסט בעברית"
    echo ""
    echo "center_print:"
    center_print "שלום עולם"
    echo ""
    echo "rtl_block (multi-line):"
    echo -e "שורה ראשונה\nשורה שנייה\nשורה שלישית" | rtl_block
}

# Functions are loaded silently - run 'rtl_demo' to see examples
