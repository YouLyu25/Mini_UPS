#!/bin/bash

world="$1"
if [ "$world" == "" ]
then
    echo "You need to specify a world"
    exit 1
fi

echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 0, 0, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 1, 1, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 2, 2, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 3, 3, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 4, 4, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 5, 5, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 6, 6, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 7, 7, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 8, 8, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 9, 9, '2018-04-23 23:00:00', true);" | psql packagesim
echo "insert into whready (wid, hid, sid, whenready, notified) values (${world}, 10, 10, '2018-04-23 23:00:00', true);" | psql packagesim
