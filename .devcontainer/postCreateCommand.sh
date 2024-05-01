#!/bin/sh
# postCreateCommand.sh

echo "START Install"

sudo chown -R vscode:vscode .
poetry config virtualenvs.in-project true
poetry install
echo "FINISH Install"