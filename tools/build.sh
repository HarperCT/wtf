#!/bin/bash

cd "$(git rev-parse --show-toplevel)"
cd python3_wtf/src

rm -rf dist build *.egg-info
python3 -m build

echo "Build distributions:"
ls -lh dist
