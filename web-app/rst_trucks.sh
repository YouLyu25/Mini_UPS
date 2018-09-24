#!/bin/bash

world="$1"
if [ "$world" == "" ]
then
    echo "You need to specify a world"
    exit 1
fi

echo "update ups_frontend_truck set status = 'I';" | psql postgres
echo "update ups_frontend_truck set package_num = '0';" | psql postgres
