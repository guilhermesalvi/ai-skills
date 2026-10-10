#!/usr/bin/env bash
# Runs a case's Python scaffold in the current, empty eval workspace.
# Usage: seed.sh <scaffold.py>
set -euo pipefail

case "${OSTYPE:-}" in
  msys* | cygwin*)
    # claude plugin eval drops LOCALAPPDATA. Without it, the Windows Python install
    # manager misses the installed interpreters and installs one into the workspace.
    export LOCALAPPDATA="${LOCALAPPDATA:-${HOMEDRIVE:-C:}${HOMEPATH:-}\\AppData\\Local}"
    ;;
esac

for python in python3 python; do
  if command -v "$python" > /dev/null &&
    "$python" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2> /dev/null; then
    exec "$python" "$1" .
  fi
done
echo "Python 3.10+ is required to seed the fixture" >&2
exit 1
