#!/bin/bash
#
# TrustRail Git Pre-Push Hook
# Scans the project for secrets before allowing a push.
#

set -e

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# TrustRail installation path (set by installer)
TRUSTRAIL_PATH="__TRUSTRAIL_PATH__"
PYTHON="__PYTHON__"
if [ -n "$TRUSTRAIL_PATH" ]; then
    export PYTHONPATH="$TRUSTRAIL_PATH:$PYTHONPATH"
fi

echo "🔍 TrustRail: Scanning for secrets before push..."

$PYTHON -m cli.main scan "$PROJECT_ROOT"
SCANNER_EXIT=$?

if [ $SCANNER_EXIT -ne 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║   ██████╗ ██╗ ██████╗ ██╗  ██╗███████╗██████╗███████╗     ║"
    echo "║   ██╔═══██╗██║██╔═══██╗██║  ██║██╔════╝██╔══██╔════╝     ║"
    echo "║   ██║   ██║██║██║  ██║███████║█████╗  ██████╔███████╗    ║"
    echo "║   ██║▄▄ ██║██║██║  ██║██╔══██║██╔══╝  ██╔══██╔════╝     ║"
    echo "║   ╚██████╔╝██║╚█████╔╝██║  ██║███████╗██║  ██║███████╗    ║"
    echo "║    ╚══▀▀▀╚═╝╚═╝ ╚════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝    ║"
    echo "║                                                              ║"
    echo "║   PUSH REJECTED: Secrets detected by TrustRail!             ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Fix the secrets or run 'trustrail fix <file>' to auto-remediate."
    echo "After fixing, review changes and try pushing again."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi

exit 0