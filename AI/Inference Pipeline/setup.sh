#! /bin/bash

# Test parameter
if [ -z "$1" ]
  then
    echo "No auth token supplied"
    exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
mkdir tmp
cd tmp
curl -O https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
./ngrok authtoken $1
cd ..
rm -r tmp