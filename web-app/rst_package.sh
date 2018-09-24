#!/bin/bash

world="$1"
if [ "$world" == "" ]
then
    echo "You need to specify a world"
    exit 1
fi

echo "delete from ups_frontend_package;" | psql postgres
