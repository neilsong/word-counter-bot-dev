#! /bin/bash

kill -2 main.py
cd word-counter-bot
source venv/bin/activate
git pull
python3 main.py