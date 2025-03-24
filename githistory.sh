#!/usr/bin/env bash

for f in {,SoftwareEngineering/}data/*_????-??-??*.md
do
    if [[ $f -nt $f.history ]]
    then
        echo Generating history for $f
        git log \
            --pretty="format:%H %ad %s" \
            --date=short \
            --follow \
            $f \
            > $f.history
#    else
#	      echo History for $f is up-to-date
    fi
done
