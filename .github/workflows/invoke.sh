#! /bin/bash

cr_output=$( git diff --name-only --diff-filter=ADMR HEAD^ "./AI/cloud-run" | grep -v *.md )

if ! [ -z "$cr_output" ]
then
    curl -X POST -H "Content-Type: application/json" "$1"
fi

ci_output=$( git diff --name-only --diff-filter=ADMR HEAD^ "./AI/cluster-inference" | grep -v *.md )
if ! [ -z "$ci_output" ]
then
    curl -X POST "$2"
fi