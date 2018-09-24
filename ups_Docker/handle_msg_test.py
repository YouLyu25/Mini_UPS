import ups_pb2
import amz_ups_pb2
import psycopg2
import threading
from concurrent.futures import ThreadPoolExecutor
import random
import time
import smtplib
from send_recv_message import send_message, recv_message
from fill_message import fill_deliveries, fill_pickups
from fill_message import fill_created_shipments, fill_arrived, fill_load_confirm
from fill_message import fill_query_results, fill_delivered


# global mutex lock
mutex = threading.Lock()
# set simspeed from 150000 to 250000 for visualize capture
simspeed = 100000
package_limit = 1

# ----------------------------------------------------------------------------------
""" 1. Amazon messages handlers """
# ----------------------------------------------------------------------------------


# handle gopickups(whid, dst_x, dst_y, packageid) message from Amazon
def handle_gopickups(world_id, amazon_conn, world_conn, amazon_msg):
    print("handle Amazon's gopickups")
    # first connect to the database shared with web app
    db_conn = psycopg2.connect("dbname='postgres' user='postgres'"
                               "host='db' port='5432'")
    db_cur = db_conn.cursor()
    command = ups_pb2.UCommands()
    command.simspeed = simspeed
    message = amz_ups_pb2.UAMessages()

    # 1. assign an available truck
    # TODO: may need to limit the max number of gopickups messages
    tracking_number = []
    i = 0
    # 1. generate shipments and tracking_number, response Amazon
    for gopickups in amazon_msg.gopickups:
        print("for gopickups in amazon_msg.gopickups")
        while 1:
            random.seed()
            tracking_number.append(random.randint(100000000, 999999999))
            # first check if the generated tracking number has already been used
            db_cur.execute("select count(*) from ups_frontend_tracking_number"
                           " where worldid = '" + str(world_id) +
                           "' and tracking_number = '" +
                           str(tracking_number[i]) + "'")
            rows = db_cur.fetchall()
            row = rows[0]
            # if tracking_number generated has not been used, use it
            if row[0] == 0:
                # update ups_frontend_tracking_number table
                db_cur.execute("insert into ups_frontend_tracking_number "
                               "(worldid, tracking_number) values ('" +
                               str(world_id) + "', '" +
                               str(tracking_number[i]) + "')")

                break
            # if tracking_number generated has been used, try again
            else:
                pass
        # get username, may need to coordinate with Amazon to set a valid one
        username = gopickups.userid
        db_cur.execute("select count(*) from auth_user where username = '" +
                       username + "'")
        rows = db_cur.fetchall()

        if not rows[0]:
            # if username does not exist, set username as "nobody"
            username = "nobody"
        else:
            # if username does not match with position_x and position_y
            db_cur.execute("select pos_x, pos_y from ups_frontend_accounts "
                           "where ups_account='" + username + "'")
            rows = db_cur.fetchall()
            if rows:
                row = rows[0]
                # if validation passed, keep username unchanged
                if gopickups.dst_x == int(row[0]) and gopickups.dst_y == int(row[1]):
                    pass
                else:
                    username = "nobody"
            # TODO: may need to response Amazon with error message or ignore
            else:
                username = "nobody"
        # add package info to database, status is created shipment
        db_cur.execute("insert into ups_frontend_package "
                       "(username, trackingid, status, position_x, "
                       "position_y, packageid, worldid) values ('" +
                       username + "', '" + str(tracking_number[i]) +
                       "', 'C', '" + str(gopickups.dst_x) + "', '" +
                       str(gopickups.dst_y) + "', '" +
                       str(gopickups.packageid) + "', '" +
                       str(world_id) + "')")

        # record the time of shipment creation
        db_cur.execute("insert into ups_frontend_time "
                       "(worldid, trackingid, c_time, packageid) values ('" +
                       str(world_id) + "', '" + str(tracking_number[i]) + "', '" +
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                       "', '" + str(gopickups.packageid) + "')")

        # update item info, store each item into database
        for things in gopickups.things:
            db_cur.execute("insert into ups_frontend_item "
                           "(worldid, trackingid, iteminfo, count) values ('" +
                           str(world_id) + "', '" + str(tracking_number[i]) + "', '"
                           + things.description + "', '" + str(things.count) + "')")

        # TODO: inform user when package is delivered
        # get username from database using packageid and worldid
        db_cur.execute("select username from ups_frontend_package where worldid='" +
                       str(world_id) + "' and packageid = '" +
                       str(gopickups.packageid) + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        username = row[0]
        # get user's email address using username
        db_cur.execute("select email from auth_user where username = '" +
                       username + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        receiver = row[0]
        # fill and send email to inform user
        host = "smtp.gmail.com"
        port = 465
        sender = "youlyu25@gmail.com"
        pwd = "abc12345678!"  # not a good practice though...
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, "Hello " + username + " !\n\nYour package's"
                   " shipment has been successfully created!")

        message = fill_created_shipments(message,
                                         tracking_number[i], gopickups.packageid)
        i = i + 1
    db_conn.commit()
    # send createdShipments message to Amazon, indicating the dispatch of truck
    send_message(amazon_conn, message)
    print("sent createdShipments message to Amazon")

    db_conn = psycopg2.connect("dbname='postgres' user='postgres'"
                               "host='db' port='5432'")
    db_cur = db_conn.cursor()
    i = 0
    for gopickups in amazon_msg.gopickups:
        truckid = 0
        # 2. assign truck to pickup package
        while 1:
            # 2.1 check if any truck is available from database
            mutex.acquire()
            # 2.1.1 first check if there is any truck with status "loaded"
            db_cur.execute("select truckid, package_num from ups_frontend_truck "
                           "where status = 'L' and worldid = '" +
                           str(world_id) + "' order by truckid asc")
            rows = db_cur.fetchall()
            # if there is a truck with status "loaded"
            if rows:
                row = rows[0]
                truckid = int(row[0])
                print("loaded truck " + str(truckid) + " found")
                # update truck status
                db_cur.execute("update ups_frontend_truck set status = 'E'"
                               " where truckid = '" + str(truckid) +
                               "' and worldid = '" + str(world_id) + "'")
                mutex.release()
                break

            # 2.1.2 if there is no truck with status "loaded", assign an "idle" one
            else:
                db_cur.execute("select truckid, package_num from ups_frontend_truck "
                               "where status = 'I' and worldid = '" +
                               str(world_id) + "' order by truckid asc")
                rows = db_cur.fetchall()
                if rows:
                    row = rows[0]
                    truckid = int(row[0])
                    print("idle truck " + str(truckid) + " found")
                    # update truck status
                    db_cur.execute("update ups_frontend_truck set status = 'E'"
                                   " where truckid = '" + str(truckid) +
                                   "' and worldid = '" + str(world_id) + "'")
                    mutex.release()
                    break
                # if there is not, keep waiting until there is an available one
                else:
                    print("no available truck")
                    mutex.release()
        # 3. update package info into database since a truck is assigned
        db_cur.execute("update ups_frontend_package set status = 'E', "
                       "truckid = '" + str(truckid) + "' where "
                       "trackingid = '" + str(tracking_number[i]) +
                       "' and worldid = '" + str(world_id) + "'")

        # EXTRA TODO: the user may be able to confirm reception?
        # 4. record the starting time of pickup
        db_cur.execute("update ups_frontend_time set e_time = '" +
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                       "' where worldid = '" + str(world_id) +
                       "' and trackingid = '" + str(tracking_number[i]) + "'")

        # 5. fill command and message for world and Amazon
        command = fill_pickups(command, truckid, gopickups.whid)
        i = i + 1

    db_conn.commit()
    # send command to the world to dispatch truck for picking up
    send_message(world_conn, command)
    print("sent pickups command to world")
    return
# ----------------------------------------------------------------------------------


# handle loaded(packageid) from Amazon
def handle_loaded(world_id, amazon_conn, world_conn, amazon_msg):
    print("handle loaded")
    # first connect to the database shared with web app
    db_conn = psycopg2.connect("dbname='postgres' user='postgres'"
                               "host='db' port='5432'")
    db_cur = db_conn.cursor()
    command = ups_pb2.UCommands()
    command.simspeed = simspeed
    message = amz_ups_pb2.UAMessages()

    for loaded in amazon_msg.loaded:
        packageid = loaded.packageid
        # TODO: may need to get truckid from database if no truckid info is provided
        db_cur.execute("select truckid from ups_frontend_package where "
                       "worldid = '" + str(world_id) + "' and packageid = '" +
                       str(packageid) + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        truckid = int(row[0])
        print("truckid = ", truckid)
        # truckid = loaded.truckid
        deliveries = command.deliveries.add()
        deliveries.truckid = truckid

        # 1.1 update truck's package_num info
        db_cur.execute("select package_num from ups_frontend_truck where worldid='"
                       + str(world_id) + "' and truckid = '" + str(truckid) + "'")
        print("2")
        rows = db_cur.fetchall()
        package_num = 0
        if rows:
            row = rows[0]
            package_num = int(row[0])
            package_num = package_num + 1
            db_cur.execute("update ups_frontend_truck set package_num = '" +
                           str(package_num) + "' where truckid = '" + str(truckid) +
                           "' and worldid = '" + str(world_id) + "'")

        # 1.2 update package info
        db_cur.execute("update ups_frontend_package set status = 'L' where "
                       "worldid = '" + str(world_id) + "' and packageid = '" +
                       str(packageid) + "'")
        print("3")
        # update loaded time of package
        db_cur.execute("update ups_frontend_time set l_time = '" +
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                       "' where worldid = '" + str(world_id) +
                       "' and packageid = '" + str(packageid) + "'")
        print("4")

        # 2. check if truck has loaded enough packages
        # if enough packages, send truck for delivery, status is "O"
        if package_num >= package_limit:
            # update truck's status to "O"
            db_cur.execute("update ups_frontend_truck set status = 'O' where "
                           "worldid = '" + str(world_id) +
                           "' and truckid = '" + str(truckid) + "'")
            print("5.0")
            # get coordinates from database using truckid
            db_cur.execute("select packageid, position_x, position_y from "
                           "ups_frontend_package where worldid = '" +
                           str(world_id) + "' and truckid = '" +
                           str(truckid) + "' and status = 'L'")
            rows = db_cur.fetchall()
            print("5.1")
            # fill deliveries command
            for row in rows:
                packages = deliveries.packages.add()
                packages.packageid = int(row[0])
                packages.x = int(row[1])
                packages.y = int(row[2])
                # set the status of these packages to "O"
                db_cur.execute("update ups_frontend_package set status = 'O' where "
                               "worldid = '" + str(world_id) + "' and packageid = '"
                               + str(packages.packageid) + "'")
                print("5.2")
                # update out for delivery time of package
                db_cur.execute("update ups_frontend_time set o_time = '" +
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                               + "' where worldid = '" + str(world_id) +
                               "' and packageid='" + str(packages.packageid) + "'")

        # not enough packages, status is "L"
        else:
            db_cur.execute("update ups_frontend_truck set status = 'L' where "
                           "worldid = '" + str(world_id) +
                           "' and truckid = '" + str(truckid) + "'")
        print("6")
        message = fill_load_confirm(message, loaded.packageid)
    print("7")
    db_conn.commit()
    # send command to the world to deliver the packages indicated by packageids
    send_message(world_conn, command)
    # send loadConfirm message to Amazon
    send_message(amazon_conn, message)
    return
# ----------------------------------------------------------------------------------


# handle queries(tracking_number) message from Amazon
def handle_queries(world_id, amazon_conn, world_conn, amazon_msg):
    print("handle queries")
    # first connect to the database shared with web app
    db_conn = psycopg2.connect("dbname='postgres' user='postgres'"
                               "host='db' port='5432'")
    db_cur = db_conn.cursor()
    # Amazon send queries to track packages
    message = amz_ups_pb2.UAMessages()
    for queries in amazon_msg.queries:
        # TODO: get truck status from DB using tracking_number
        db_cur.execute("select status from ups_frontend_package where "
                       "worldid = '" + str(world_id) + "' and trackingid = '" +
                       str(queries.tracking_number) + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        status = row[0]
        # fill queryResults message
        message = fill_query_results(message, queries.tracking_number, status)
    # send message to Amazon indicating the status of truck/package
    send_message(amazon_conn, message)
    return
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
""" 2. world messages handlers """
# ----------------------------------------------------------------------------------


# handle completions(truckid, x, y) message from world
def handle_completions(world_id, amazon_conn, world_conn, world_msg):
    print("handle completions")
    # first connect to the database shared with web app
    db_conn = psycopg2.connect("dbname='postgres' user='postgres'"
                               "host='db' port='5432'")
    db_cur = db_conn.cursor()
    # determine if the truck has finished all the deliveries
    # or it reaches the warehouse by checking the current status
    # of the truck stored in the database
    for completions in world_msg.completions:
        message = amz_ups_pb2.UAMessages()
        # check truck's current status
        # if 'O', then it has finished all the deliveries
        print("a")
        db_cur.execute("select status from ups_frontend_truck where "
                       "worldid = '" + str(world_id) + "' and truckid = '" +
                       str(completions.truckid) + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        truck_status = row[0]
        # the truck has finished all its tasks, it is now idle
        if truck_status is "O":
            print("b")
            # update the status of truck to idle in the database
            db_cur.execute("update ups_frontend_truck set status = 'I', "
                           "package_num = '0' where "
                           "worldid = '" + str(world_id) + "' and truckid = '" +
                           str(completions.truckid) + "'")
        # else if en route, it just reaches the warehouse
        elif truck_status is "E":
            print("c")
            # update the status of truck
            db_cur.execute("update ups_frontend_truck set status = 'W' where "
                           "worldid = '" + str(world_id) + "' and truckid = '" +
                           str(completions.truckid) + "'")
            # TODO: get packageid from DB using truckid in completions
            db_cur.execute("select packageid from ups_frontend_package where "
                           "worldid = '" + str(world_id) + "' and truckid = '" +
                           str(completions.truckid) + "' and status = 'E'")
            rows = db_cur.fetchall()
            row = rows[0]
            packageid = int(row[0])
            message = fill_arrived(message, packageid, completions.truckid)
            # the truck reaches warehouse, notify Amazon with arrived message
            send_message(amazon_conn, message)
            print("d")
            # update status of package
            db_cur.execute("update ups_frontend_package set status = 'W' where "
                           "packageid = '" + str(packageid) +
                           "' and worldid = '" + str(world_id) + "'")
            print("e")
            # update status of waiting for load time
            db_cur.execute("update ups_frontend_time set w_time = '" +
                           time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                           "' where worldid = '" + str(world_id) +
                           "' and packageid = '" + str(packageid) + "'")
    print("f")
    db_conn.commit()
    return
# ----------------------------------------------------------------------------------


# handle delivered(truckid, packageid) message from world
def handle_delivered(world_id, amazon_conn, world_conn, world_msg):
    print("handle delivered")
    # first connect to the database shared with web app
    db_conn = psycopg2.connect("dbname='postgres' user='postgres'"
                               "host='db' port='5432'")
    db_cur = db_conn.cursor()
    # a certain package has been delivered
    message = amz_ups_pb2.UAMessages()
    for delivered in world_msg.delivered:
        # find tracking_number in the database using packageid
        db_cur.execute("select trackingid from ups_frontend_package where "
                       "worldid = '" + str(world_id) + "' and truckid = '" +
                       str(delivered.truckid) + "' and packageid = '" +
                       str(delivered.packageid) + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        tracking_number = int(row[0])
        # update the status of package to delivered
        db_cur.execute("update ups_frontend_package set status = 'D' where "
                       "worldid = '" + str(world_id) + "' and trackingid = '" +
                       str(tracking_number) + "'")
        # update delivered time
        db_cur.execute("update ups_frontend_time set d_time = '" +
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                       "' where worldid = '" + str(world_id) +
                       "' and trackingid = '" + str(tracking_number) + "'")
        # decrement truck's package_num as one package has been delivered
        db_cur.execute("select package_num from ups_frontend_truck where "
                       "worldid = '" + str(world_id) + "' and truckid = '" +
                       str(delivered.truckid) + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        package_num = int(row[0])
        package_num = package_num - 1
        db_cur.execute("update ups_frontend_truck set package_num = '" +
                       str(package_num) + "' where "
                       "worldid = '" + str(world_id) + "' and truckid = '" +
                       str(delivered.truckid) + "'")

        # TODO: inform user when package is delivered
        # get username from database using packageid and worldid
        db_cur.execute("select username, position_x, position_y from "
                       "ups_frontend_package where worldid = '" +
                       str(world_id) + "' and packageid = '" +
                       str(delivered.packageid) + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        username = row[0]
        x = row[1]
        y = row[2]
        # get user's email address using username
        db_cur.execute("select email from auth_user where username = '" +
                       username + "'")
        rows = db_cur.fetchall()
        row = rows[0]
        receiver = row[0]
        # fill and send email to inform user
        host = "smtp.gmail.com"
        port = 465
        sender = "youlyu25@gmail.com"
        pwd = "abc12345678!"  # not a good practice though...
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, "Hello " + username + " !\n\nYour package"
                   " has been successfully delivered to (" + x + ", " + y + ") !")

        message = fill_delivered(message, delivered.packageid)
    db_conn.commit()
    # send message to Amazon to notify that a package's delivery is complete
    send_message(amazon_conn, message)

# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
""" 3. Amazon and world message main handlers """
# ----------------------------------------------------------------------------------


# parse message from Amazon and make corresponding operations
def handle_amazon_msg(world_id, amazon_conn, world_conn, amazon_msg):
    print("handle_amazon_msg\n", amazon_msg)
    """
        there are three possible messages sent from Amazon:
        GoPickUp            gopickups
        LoadSuccess         loaded
        GetDeliveryStatus   queries
        parse the message and determine which operation to make
    """
    # TODO: how should UPS handle error in amazon_msg?
    # TODO: may need to coordinate a set of uniform error messages
    # if error:
    if len(amazon_msg.gopickups):
        handle_gopickups(world_id, amazon_conn, world_conn, amazon_msg)
    if len(amazon_msg.loaded):
        handle_loaded(world_id, amazon_conn, world_conn, amazon_msg)
    if len(amazon_msg.queries):
        handle_queries(world_id, amazon_conn, world_conn, amazon_msg)
    return


# parse message from Amazon and make corresponding operations
def handle_world_msg(world_id, amazon_conn, world_conn, world_msg):
    print("handle_world_msg\n", world_msg)
    """
        there are two possible messages sent from the world:
        UFinished       completions
        UDeliveryMade   delivered
        parse the message and determine which operations to make
    """
    # TODO: how should UPS handle error in world_msg?
    # TODO: try to check all the error information
    # if error:
    if len(world_msg.completions):
        handle_completions(world_id, amazon_conn, world_conn, world_msg)
    if len(world_msg.delivered):
        handle_delivered(world_id, amazon_conn, world_conn, world_msg)
    return


# ----------------------------------------------------------------------------------
""" 4. Amazon and world message receiving threads """
# ----------------------------------------------------------------------------------


# receive messages from Amazon
def recv_amazon_msg(world_id, amazon_conn, world_conn):
    print("recv_amazon_msg")
    # create a thread pool to handle received messages
    num_threads = 5
    # pool = threadpool.ThreadPool(num_threads)
    pool = ThreadPoolExecutor(num_threads)
    while 1:
        # receive a message from Amazon and assign a thread to handle it
        amazon_msg = recv_message(amazon_conn, amz_ups_pb2.AUMessages)
        pool.submit(handle_amazon_msg, world_id, amazon_conn, world_conn, amazon_msg)
# ----------------------------------------------------------------------------------


# receive messages from world
def recv_world_msg(world_id, amazon_conn, world_conn):
    print("recv_world_msg")
    # create a thread pool to handle received messages
    num_threads = 5
    pool = ThreadPoolExecutor(num_threads)
    while 1:
        # receive a message from Amazon and assign a thread to handle it
        world_msg = recv_message(world_conn, ups_pb2.UResponses)
        pool.submit(handle_world_msg, world_id, amazon_conn, world_conn, world_msg)
