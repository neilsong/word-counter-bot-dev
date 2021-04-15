#! /bin/bash

cd /word-counter-bot-dev/"$1"

format_commit_msg=$( git log -1 --pretty=%B | grep -o "Fix code style issues with Black" )

if ! [ -z "$format_commit_msg" ]
then exit 0
fi

pid=$( cat pid )

sudo -S kill -INT $pid

status=$( ps -ef | grep "$pid" | grep -v grep | awk '{print $2}' )

while ! [ -z "$status" ]
do sleep 0.2 & status=$( ps -ef | grep "$pid" | grep -v grep | awk '{print $2}' )
done

source $HOME/.profile

poetry install
poetry run python3 main.py
