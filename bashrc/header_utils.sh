#!/usr/bin/env bash

# Create this file as ~/.config/bash/header_utils.sh
# then source the file in .bashrc

# Guard against being sourced multiple times
if ! declare -F add_or_update_header >/dev/null; then
add_or_update_header() {
    local file="$1"
    local new_author="${2:-$(whoami)}"
    local new_desc="$3"

    if [[ -z "$file" ]]; then
        echo "Usage: add_or_update_header <file> [author] [description]" >&2
        return 1
    fi

    local perms=""
    [[ -f "$file" ]] && perms=$(stat -c '%a' "$file" 2>/dev/null || stat -f '%Lp' "$file")

    local tmp body shebang firstline
    tmp=$(mktemp) || return 1
    body=$(mktemp) || { rm -f "$tmp"; return 1; }

    if [[ -f "$file" ]]; then
        read -r firstline < "$file"
        if [[ "$firstline" =~ ^#! ]]; then
            shebang="$firstline"
            tail -n +2 "$file" > "$body"
        else
            cat "$file" > "$body"
        fi
    else
        : > "$body"
    fi

    if grep -q "^# File: $(basename "$file")$" "$file" 2>/dev/null; then
        awk -v author="$new_author" \
            -v desc="$new_desc" \
            -v update_desc="$([[ -n "$new_desc" && "$new_desc" != "-" ]] && echo 1 || echo 0)" \
            -v now="$(date '+%Y-%m-%d %H:%M:%S')" '
            BEGIN { in_hdr=1; seen_date=0 }
            NR==1 && $0 ~ /^#!/ { print; next }
            {
                if (in_hdr) {
                    if ($0 ~ /^#\s*$/) {
                        if (!seen_date) {
                            print "# Created On: " strftime("%Y-%m-%d %H:%M:%S")
                        }
                        if (!seen_lastmod) {
                            print "# Last Modified: " now
                        }
                        if (update_desc && !seen_desc) {
                            print "# Description: " desc
                        }
                        print
                        in_hdr=0
                        next
                    }

                    if ($0 ~ /^# *Created On:/) {
                        seen_date=1
                        print
                        next
                    }
                    if ($0 ~ /^# *Date Created:/) {
                        dateval=$0; sub(/^# *Date Created: */, "", dateval)
                        print "# Created On: " dateval
                        seen_date=1
                        next
                    }
                    if ($0 ~ /^# *Date:/) {
                        dateval=$0; sub(/^# *Date: */, "", dateval)
                        print "# Created On: " dateval
                        seen_date=1
                        next
                    }

                    if ($0 ~ /^# *Author:/) {
                        print "# Author: " author
                        next
                    }

                    if ($0 ~ /^# *Last Modified:/) {
                        print "# Last Modified: " now
                        seen_lastmod=1
                        next
                    }

                    if ($0 ~ /^# *Description:/) {
                        if (update_desc) {
                            print "# Description: " desc
                        } else {
                            print
                        }
                        seen_desc=1
                        next
                    }

                    print
                    next
                }
                print
            }' "$file" > "$tmp"
    else
        {
            [[ -n "$shebang" ]] && echo "$shebang"
            echo "# File: $(basename "$file")"
            echo "# Author: $new_author"
            echo "# Created On: $(date '+%Y-%m-%d %H:%M:%S')"
            echo "# Last Modified: $(date '+%Y-%m-%d %H:%M:%S')"
            echo "# Description: ${new_desc:-TODO: Add description}"
            echo "#"
            echo
            cat "$body"
        } > "$tmp"
    fi

    mv "$tmp" "$file"
    rm -f "$body"
    [[ -n "$perms" ]] && chmod "$perms" "$file"
}
fi
