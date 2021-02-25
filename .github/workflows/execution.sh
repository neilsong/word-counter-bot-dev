#! /bin/bash
cd /home/azureuser/word-counter-bot-dev/
source .venv/bin/activate
/root/.poetry/bin/poetry install --no-dev
/root/.poetry/bin/poetry run python3 main.py