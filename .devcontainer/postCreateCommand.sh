#!/bin/sh
# postCreateCommand.sh

echo "START Install"

# Install gcp client
sudo apt-get update -y
sudo apt-get install apt-transport-https ca-certificates gnupg curl -y
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-cli -y

# Install Poetry
sudo chown -R vscode:vscode .
poetry config virtualenvs.in-project true
poetry install --with test,docs,dev,typing
source .venv/bin/activate
echo "FINISH Install"