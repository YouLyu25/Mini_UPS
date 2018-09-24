from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.decoder import _DecodeVarint32


# encode the data to be sent to the "world"
def encode_varint(value):
    """ Encode an int as a protobuf varint """
    data = []
    _VarintEncoder()(data.append, value, None)
    return b''.join(data)


# decode the data received from the "world"
def decode_varint(data):
    """ Decode a protobuf varint to an int """
    return _DecodeVarint32(data, 0)[0]


# send protocol buffer messages over TCP
def send_message(conn, msg):
    """ Send a message, prefixed with its size, to a TPC/IP socket """
    data = msg.SerializeToString()
    size = encode_varint(len(data))
    conn.sendall(size + data)


# receive and parse message sent from the "world"
def recv_message(conn, msg_type):
    """ Receive a message, prefixed with its size, from a TCP/IP socket """
    # Receive the size of the message data
    data = b''
    while True:
        try:
            data += conn.recv(1)
            size = decode_varint(data)
            break
        except IndexError:
            pass
    # Receive the message data
    data = conn.recv(size)
    # Decode the message
    msg = msg_type()
    msg.ParseFromString(data)
    return msg
