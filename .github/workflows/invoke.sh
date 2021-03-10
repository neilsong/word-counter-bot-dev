#! /bin/bash

output=$( git diff --name-only --diff-filter=ADMR HEAD^ "./AI/Cloud Run" )

if ! [ -z "$output" ]
then
    curl -X POST -H "Content-Type: application/json" "$1"
fi