#!/usr/bin/env python3
import socket
import amazon_pb2
import amz_ups_pb2
from send_recv_message import send_message, recv_message
# from fill_message import fill_amazon_connect, fill_load, fill_au_connected
# from fill_message import fill_gopickups, fill_loaded, fill_queries

warehouse_id = 1
# ups_host = "vcm-3838.vm.duke.edu"
ups_host = "localhost"
ups_port = 6669


def fill_amazon_connect(worldid, num_wh):
    amazon_connect = amazon_pb2.AConnect()
    amazon_connect.worldid = worldid
    x = 100
    y = 100
    for i in range(0, num_wh):
        initwh = amazon_connect.initwh.add()
        initwh.x = x
        initwh.y = y
        x = x + 10
        y = y + 10
    print(amazon_connect)
    return amazon_connect


# Amazon command to load package
def fill_load(message, whnum, truckid, shipid):
    load = message.load.add()
    load.whnum = whnum
    load.truckid = truckid
    load.shipid = shipid
    return message


def fill_au_connected(message):
    return message


def fill_gopickups(message, whid, dst_x, dst_y, packageid):
    gopickups = message.gopickups.add()
    gopickups.whid = whid
    gopickups.dst_x = dst_x
    gopickups.dst_y = dst_y
    gopickups.packageid = packageid
    gopickups.userid = "yl489"
    things1 = gopickups.things.add()
    things1.id = 0
    things1.description = "fancy stuff"
    things1.count = 2
    things2 = gopickups.things.add()
    things2.id = 1
    things2.description = "crap"
    things2.count = 3
    return message


def fill_loaded(message, packageid):
    loaded = message.loaded.add()
    loaded.packageid = packageid
    return message


def fill_queries(message, tracking_number):
    queries = message.queries.add()
    queries.tracking_number = tracking_number
    return message


""" ENTRY """
""" 1. establish connection with UPS """
# establish a TCP connection to UPS
ups_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while 1:
    try:
        # ups_conn.connect((ups_host, ups_port))
        ups_conn.connect((ups_host, ups_port))
        print("connected to ups server!")
        break
    except (ConnectionRefusedError, ConnectionResetError,
            ConnectionError, ConnectionAbortedError) as error:
        print(error)
        continue

""" 2. receive UAConnect message from UPS """
UAConnect = recv_message(ups_conn, amz_ups_pb2.UAConnect)
print("UAConnect\n", UAConnect)

""" 3. send AUConnected message to UPS """
message = amz_ups_pb2.AUConnected()
message = fill_au_connected(message)
send_message(ups_conn, message)
print("sent AUConnected")

""" 4. connect to the world and init warehouse information """
# establish a TCP connection to UPS
world_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while 1:
    try:
        # world_conn.connect(('localhost', 23456))

        # -----------------------------------------------------------------------------------------
        world_conn.connect(('vcm-3838.vm.duke.edu', 23456))
        # -----------------------------------------------------------------------------------------

        print("connected to the world!")
        break
    except (ConnectionRefusedError, ConnectionResetError,
            ConnectionError, ConnectionAbortedError) as error:
        print(error)
        continue

# send AConnect message
num_wh = 30
worldid = int(UAConnect.worldid)
AConnect = fill_amazon_connect(worldid, num_wh)
send_message(world_conn, AConnect)
AConnected = recv_message(world_conn, amazon_pb2.AConnected)
print(AConnected)

""" 5. send gopickups, loaded and queries messages to UPS """
# send gopickups message

whid = warehouse_id
packageid = whid
shipid = whid

message = amz_ups_pb2.AUMessages()
message = fill_gopickups(message, whid=whid, dst_x=10, dst_y=10, packageid=packageid)
# message = fill_gopickups(message, whid=whid + 1, dst_x=10, dst_y=10, packageid=packageid + 1)
# message = fill_gopickups(message, whid=whid+2, dst_x=30, dst_y=30, packageid=packageid+2)
send_message(ups_conn, message)
print("sent gopickups")
res = recv_message(ups_conn, amz_ups_pb2.UAMessages)
tracking_number1 = res.createdShipments[0].tracking_number
# tracking_number2 = res.createdShipments[1].tracking_number
print(res)

# receive TruckArrived message from UPS
arrived1 = recv_message(ups_conn, amz_ups_pb2.UAMessages)
truckid1 = arrived1.arrived[0].truckid
print(arrived1)
# arrived2 = recv_message(ups_conn, amz_ups_pb2.UAMessages)
# truckid2 = arrived2.arrived[0].truckid
# print(arrived2)
# if truckid1 > truckid2:
#    temp = truckid1
#    truckid1 = truckid2
#    truckid2 = temp

# send load package command
message = amazon_pb2.ACommands()
message = fill_load(message, whnum=whid, truckid=truckid1, shipid=shipid)
# message = fill_load(message, whnum=whid + 1, truckid=truckid2, shipid=shipid + 1)
# message = fill_load(message, whnum=whid+2, truckid=truckid+2, shipid=shipid+2)
send_message(world_conn, message)
loaded = recv_message(world_conn, amazon_pb2.AResponses)
print(loaded)

# send loaded message
message = amz_ups_pb2.AUMessages()
message = fill_loaded(message, packageid=packageid)
# message = fill_loaded(message, packageid=packageid+1)
# message = fill_loaded(message, packageid=packageid+2)
send_message(ups_conn, message)
print("sent loaded")
loadedConfirm = recv_message(ups_conn, amz_ups_pb2.UAMessages)
print(loadedConfirm)

while 1:
    res = recv_message(ups_conn, amz_ups_pb2.UAMessages)
    print(res)
    if res.delivered:
        # send queries message
        message = amz_ups_pb2.AUMessages()
        message = fill_queries(message, tracking_number1)
        send_message(ups_conn, message)
        print("sent queries")
        queryResults = recv_message(ups_conn, amz_ups_pb2.UAMessages)
        print(queryResults)
