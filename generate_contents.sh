#!/usr/bin/env bash

for f in Books{,BackLog}
do
    echo Generating JSON contents for $f
    ./${f}_json.cgi --no-headers > ${f}.json
done

for f in Books
do
    echo Generating ATOM contents for $f
    ./${f}_atom.cgi --no-headers > ${f}.atom
done

for f in Books{,BackLog} Journal
do
    echo Generating JSON contents for SoftwareEngineering/$f
    (
        cd SoftwareEngineering
        ./${f}_json.cgi --no-headers > ${f}.json
    )
done

for f in Books Journal
do
    echo Generating ATOM contents for SoftwareEngineering/$f
    (
        cd SoftwareEngineering
        ./${f}_atom.cgi --no-headers > ${f}.atom
    )
done
