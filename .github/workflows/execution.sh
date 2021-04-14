#! /bin/bash

cd /word-counter-bot-dev/"$1"

if [ -z $(git log -1 --pretty=%B | grep -o "Fix code style issues with Black") ]
then exit 0
fi

pid=$( cat pid )

kill -INT $pid

while ! [ -z $( ps -ef | grep "$pid" | grep -v grep | awk '{print $2}' ) ]
do sleep 0.2
done

source $HOME/.profile

poetry install
poetry run python3 main.py
