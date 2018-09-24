import ups_pb2
import amazon_pb2
import amz_ups_pb2


def fill_ups_connect(reconnectid, numtrucksinit):
    ups_connect = ups_pb2.UConnect()
    # TODO: may need to make reconnectid as user input
    if reconnectid:
        ups_connect.reconnectid = reconnectid
        return ups_connect
    if numtrucksinit:
        ups_connect.numtrucksinit = numtrucksinit
    return ups_connect


def fill_ua_connect(worldid):
    ua_connect = amz_ups_pb2.UAConnect()
    ua_connect.worldid = worldid
    return ua_connect


# fill UGoDeliver deliveries in UCommands
def fill_deliveries(command, truckid, packageid, x, y):
    deliveries = command.deliveries.add()
    deliveries.truckid = truckid
    packages = deliveries.packages.add()
    packages.packageid = packageid
    packages.x = x
    packages.y = y
    return command


# fill UGoPickup pickups in UCommands
def fill_pickups(command, truckid, whid):
    pickups = command.pickups.add()
    pickups.truckid = truckid
    pickups.whid = whid
    return command


# fill PackageReqAck createdShipments
def fill_created_shipments(message, tracking_number, packageid):
    created_shipments = message.createdShipments.add()
    created_shipments.tracking_number = tracking_number
    created_shipments.packageid = packageid
    return message


# fill TruckArrived arrived
def fill_arrived(message, packageid, truckid):
    arrived = message.arrived.add()
    arrived.packageid = packageid
    arrived.truckid = truckid
    return message


# fill LoadConfirmation loadConfirm
def fill_load_confirm(message, packageid):
    load_confirm = message.loadedConfirm.add()
    load_confirm.packageid = packageid
    return message


# fill ReturnDeliveryStatus queryResults
def fill_query_results(message, tracking_number, status):
    query_results = message.queryResults.add()
    query_results.tracking_number = tracking_number
    query_results.status = status
    return message


# fill DeliveryComplete
def fill_delivered(message, packageid):
    delivered = message.delivered.add()
    delivered.packageid = packageid
    return message


''' following messages are for debugging only '''


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
