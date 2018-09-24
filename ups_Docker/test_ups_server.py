#!/usr/bin/env python3
import socket
import psycopg2
import threading
import ups_pb2
import amz_ups_pb2
from send_recv_message import send_message, recv_message
from handle_msg import recv_amazon_msg, recv_world_msg
from fill_message import fill_ups_connect, fill_ua_connect


""" MAIN ENTRY """
conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' port='5432' password='psql'")
print("connected to the database!")

""" 1. establish connection with the world """
# establish a TCP connection to the "world"
world_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while 1:
    try:
        world_conn.connect(('vcm-3838.vm.duke.edu', 12345))
        break
    except (ConnectionRefusedError, ConnectionResetError,
            ConnectionError, ConnectionAbortedError) as error:
        print(error)
        continue

# 1.1 first check the database to see if there is any created world
# TODO: get created world's id from the data base, default 1000
"""
   database lookup here->
"""
world_id = 1000
num_trucks = 10
while 1:
    try:
        if 0:
            # TODO: if world already created, reconnect to the world:
            UConnect = fill_ups_connect(world_id, None)
            send_message(world_conn, UConnect)
        else:
            # TODO: else, if world is not created, create and init world:
            UConnect = fill_ups_connect(None, num_trucks)
            send_message(world_conn, UConnect)
            res = recv_message(world_conn, ups_pb2.UConnected)
            world_id = res.worldid
            print(res)
            # apart from the worldid, world also responses init info for trucks
            print("init trucks:\n")
            for i in range(0, num_trucks):
                res = recv_message(world_conn, ups_pb2.UResponses)
                print(res)
        break
    except (ConnectionRefusedError, ConnectionResetError,
            ConnectionError, ConnectionAbortedError):
        continue
if not str(res).count("error"):
    print("connected to the world\n" + str(res))
else:
    print("Error: cannot connect to the world, " + str(res) + "\n")
    world_conn.close()
    amazon_conn.close()
    exit(0)


""" 2. establish connection with Amazon """
# 2.1 listen and accept connection from Amazon
amazon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# TODO: determine the port used for A/U communication, use 6666 temporarily
amazon_socket.bind(('0.0.0.0', 6666))
amazon_socket.listen(6)
print("waiting for Amazon's connection...")
# accept Amazon's connection
amazon_conn, address = amazon_socket.accept()
print('Connected with ' + address[0] + ':' + str(address[1]))

# 2.2 send UAConnect message to Amazon, indicating world_id, and receive AUConnected message
UAConnect = fill_ua_connect(world_id)
send_message(amazon_conn, UAConnect)
print("sent UAConnect")
res = recv_message(amazon_conn, amz_ups_pb2.AUConnected)
print("AUConnected\n", res)
if not str(res).count("error"):
    print("connected to the world\n" + str(res))
else:
    print("Error: cannot connect to the world, " + str(res) + "\n")
    world_conn.close()
    amazon_conn.close()
    exit(0)


""" 3. receive messages from Amazon and world, handle the messages """
# create two threads to handle messages from amazon and world respectively
thread1 = threading.Thread(target=recv_amazon_msg, args=(amazon_conn, world_conn,))
thread1.start()
thread2 = threading.Thread(target=recv_world_msg, args=(amazon_conn, world_conn,))
thread2.start()
while 1:
    pass
