import time

def _packet(id, data):
    return (0, id, bytes(data))

def _close(id):
    return (-1, id)

def recv_socket(s, q, id, lenbytes=2):
    overflowData = bytearray()
    while True:
        time.sleep(0.02)
        working = True
        packetSize = -1
        data = bytearray()
        data += overflowData
        overflowData = bytearray()
        while working:
            datum = s.recv(1024)
            if len(datum) == 0:
                s.close()
                # q.put(_close(id))
                return
            data += datum
            if len(data) >= packetlen and packetSize == -1:
                packetSize = int.from_bytes(data[:lenbytes], 'big')
                data = data[lenbytes:]
            working = packetSize == -1 or len(data) < packetSize
        message = data[:packetSize]
        q.put(_packet(id, message))
        overflowData = data[packetSize:]