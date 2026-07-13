#!/usr/bin/env bash
# run_lab.sh - easy invocation wrapper for python-stdlib-interpreter-pool-isolation-footgun-lab
set -euo pipefail
cd "$(dirname "$0")"

# interpreter discovery: $PYTHON_BIN, then python3.14, python3, python
if [ -n "${PYTHON_BIN:-}" ] && command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    PY="$PYTHON_BIN"
elif command -v python3.14 >/dev/null 2>&1; then
    PY=python3.14
elif command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    PY=python
else
    echo "error: no python interpreter found (tried \$PYTHON_BIN, python3.14, python3, python)" >&2
    exit 1
fi

echo "Using: $($PY --version 2>&1) at $(command -v "$PY")"
echo

echo "==> syntax check"
"$PY" -m py_compile run_lab.py worker_tasks.py test_lab.py
echo "compile ok"
echo

echo "==> run_lab"
"$PY" run_lab.py
echo

echo "==> unittest"
"$PY" -m unittest -v
