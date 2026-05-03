#!/bin/bash
find . -name "*.py" -not -path "./.venv/*" -not -path "./99_Backup/*" | sort | while read f; do
    echo "=== $f ==="
    cat "$f"
    echo ""
done > codebasis.txt && ls -lh codebasis.txt