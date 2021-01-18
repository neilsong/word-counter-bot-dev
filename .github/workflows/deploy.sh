#! /bin/bash
cd /home/azureuser/word-counter-bot
screen -X quit
source venv/bin/activate
git pull
screen -d -m python3 main.py
exit;