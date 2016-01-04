:#!/bin/sh
# Usage: ./remove_orphans.sh [-f]

[ "$1" = "-f" ] && REMOVE=1
 
IFS='
'
for db in music video photo; do
    for testfile in `/usr/syno/pgsql/bin/psql mediaserver admin -tA -c "select path from $db;"`; do
        if [ ! -f "$testfile" ]; then
            echo "MISSING: $testfile"
            [ -n "$REMOVE" ] && synoindex -d "$testfile"
        fi
    done
done