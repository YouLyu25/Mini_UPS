#!/usr/bin/env python3
import socket
import threading

import psycopg2

import ups_pb2
import amz_ups_pb2
from send_recv_message import send_message, recv_message
from handle_msg_test import recv_amazon_msg, recv_world_msg
from fill_message import fill_ups_connect, fill_ua_connect


""" MAIN ENTRY """
""" connect to the database which is shared with web app """
while 1:
    try:
        db_conn = psycopg2.connect("dbname='postgres' user='postgres'"
                                   "host='vcm-3838.vm.duke.edu' port='6666'")
        db_cur = db_conn.cursor()
        print("connected to the database!")
        break
    except psycopg2.OperationalError as error:
        print(error)
        continue


# ----------------------------------------------------------------------------------
""" 1. establish connection with the world """
# ----------------------------------------------------------------------------------
# 1.1 establish a TCP connection to the "world"
world_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while 1:
    try:
        world_conn.connect(('world', 12345))
        break
    except (ConnectionRefusedError, ConnectionResetError,
            ConnectionError, ConnectionAbortedError) as error:
        print(error)
        continue

# 1.2 check the database to see if there is any created world
# TODO: get created world's id from the data base, default 1000
#       database lookup here->
# TODO: for now, use a created world 1339 for debugging
world_id = 1871
num_trucks = 50
while 1:
    try:
        # TODO: first, check curr_world table, see if any world has been created
        db_cur.execute("select worldid from ups_frontend_curr_world "
                       "where name = 'curr_world'")
        rows = db_cur.fetchall()
        if rows:
            row = rows[0]
            # TODO: if a world is already created, reconnect to the world:
            print("reconenct to the world")
            world_id = int(row[0])
            UConnect = fill_ups_connect(world_id, None)
            send_message(world_conn, UConnect)
            res = recv_message(world_conn, ups_pb2.UResponses)
            print(res)
        else:
            # TODO: else, if world is not created, create and init world:
            # send UConnect message without worldid to the world to init a world
            print("first time run, create a new world")
            UConnect = fill_ups_connect(None, num_trucks)
            send_message(world_conn, UConnect)
            res = recv_message(world_conn, ups_pb2.UConnected)
            print(res)
            world_id = res.worldid
            # update the current world info
            db_cur.execute("insert into ups_frontend_curr_world (name, worldid) "
                           "values ('curr_world', " + str(world_id) + ")")
            # apart from the worldid, world also responses init info for trucks
            print("init trucks:\n")
            for i in range(0, num_trucks):
                res = recv_message(world_conn, ups_pb2.UResponses)
                print(res)
                # add truck init info into database, all idle
                db_cur.execute("insert into ups_frontend_truck "
                               "(worldid, truckid, status, package_num) values ("
                               + str(world_id) + ", " + str(i) + ", " + "'I', 0)")
            pass
        break
    except (ConnectionRefusedError, ConnectionResetError,
            ConnectionError, ConnectionAbortedError):
        continue
if not str(res).count("error"):
    print("connected to the world")
else:
    print("error: cannot connect to the world, " + str(res) + "\n")
    world_conn.close()
    exit(0)
db_conn.commit()


# ----------------------------------------------------------------------------------
""" 2. establish connection with Amazon """
# ----------------------------------------------------------------------------------
# 2.1 listen and accept connection from Amazon
amazon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# TODO: determine the port used for A/U communication, use 6669 temporarily
amazon_socket.bind(('0.0.0.0', 6669))
amazon_socket.listen(1)
print("waiting for Amazon's connection...")
# accept Amazon's connection
amazon_conn, address = amazon_socket.accept()
print('Connected with ' + address[0] + ':' + str(address[1]))

# 2.2 send UAConnect message to Amazon and receive AUConnected message
while 1:
    # inform Amazon with current worldid
    UAConnect = fill_ua_connect(world_id)
    send_message(amazon_conn, UAConnect)
    print("sent UAConnect")
    res = recv_message(amazon_conn, amz_ups_pb2.AUConnected)
    print("AUConnected\n", res)
    if not str(res).count("error"):
        print("connected to Amazon\n" + str(res))
        break
    else:
        print("error: cannot connect to Amazon, " + str(res) + "\n")
        continue


# ----------------------------------------------------------------------------------
""" 3. receive messages from Amazon and world, handle the messages """
# ----------------------------------------------------------------------------------
# create two threads to handle messages from amazon and world respectively
thread1 = threading.Thread(target=recv_amazon_msg, args=(world_id, amazon_conn, world_conn,))
thread1.start()
thread2 = threading.Thread(target=recv_world_msg, args=(world_id, amazon_conn, world_conn,))
thread2.start()
while 1:
    pass


