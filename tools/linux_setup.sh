#!/bin/bash

sudo apt install \
    python3 \
    python3-build \
    python3-pytest \
    python3-pytest-cov \
    python3-setuptools \
    python3-setuptools-scm \
    python3-flake8

REPO_ROOT=$(git rev-parse --show-toplevel) || {
    echo "Not a git repository!"
    exit 1
}

HOOKS_SCRIPT="$REPO_ROOT/tools/install_git_hooks.sh"

if [ -f "$HOOKS_SCRIPT" ]; then
    bash "$HOOKS_SCRIPT"
else
    echo "$HOOKS_SCRIPT not found, skipping git hooks installation."
fi

echo "Setup complete."
