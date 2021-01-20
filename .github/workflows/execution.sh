#! /bin/bash
mkdir /home/azureuser
cd /home/azureuser/word-counter-bot-dev/
git clone https://github.com/neilsong/word-counter-bot-dev.git
source /home/azureuser/word-counter-bot-dev/venv/bin/activate
python3 /home/azureuser/word-counter-bot-dev/main.py