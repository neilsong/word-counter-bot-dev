#! /bin/bash
cd /home/azureuser/word-counter-bot-dev/
source .venv/bin/activate
poetry install
poetry run python3 main.py