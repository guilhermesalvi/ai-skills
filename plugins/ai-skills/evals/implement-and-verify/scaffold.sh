#!/usr/bin/env bash
# Seeds this case from scaffold.py, shared with the offline fixture tests.
exec bash "$(dirname "$0")/../seed.sh" "$(dirname "$0")/scaffold.py"
