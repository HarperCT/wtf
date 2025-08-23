#!/bin/sh

REPO_ROOT=$(git rev-parse --show-toplevel) || {
    echo "Not a git repository!"
    exit 1
}

HOOKS_SRC="$REPO_ROOT/tools/git_hooks"
HOOKS_DEST="$REPO_ROOT/.git/hooks"

if [ ! -d "$HOOKS_SRC" ]; then
    echo "Hooks source folder '$HOOKS_SRC' does not exist!"
    exit 1
fi

echo "Copying hooks from $HOOKS_SRC to $HOOKS_DEST"
cp -r "$HOOKS_SRC/"* "$HOOKS_DEST/"

echo "Successfully installed git hooks."
