#! /bin/bash
cd /home/azureuser/word-counter-bot-dev/

pid=$( cat pid )

kill -INT $pid

while ! [ -z $( ps -ef | grep "$pid" | grep -v grep | awk '{print $2}' ) ]
do sleep 0.2
done

/root/.poetry/bin/poetry install --no-dev
/root/.poetry/bin/poetry run python3 main.py