#!/usr/bin/env python3
# coding: utf-8

# Created by Álvaro Justen <https://github.com/turicas>

import random
import socket


client = socket.socket(socket.AF_INET,
                       socket.SOCK_SEQPACKET,
                       socket.IPPROTO_SCTP)

message = b'my msg ' + bytes(str(random.randint(0, 9)), 'ascii')
server_address = ('127.0.0.1', 1234)
bytes_sent = client.sendmsg([message], [], socket.MSG_EOR, server_address)
print('Sent {} bytes to {}: {}'.format(bytes_sent, server_address, ''))

print('Waiting for response...')
buffer = b''
flags = None
while flags != socket.MSG_EOR:
    data, ancillary_data, flags, sender = client.recvmsg(1024)
    buffer += data
print('Received from {}: {}'.format(sender, buffer))

client.close()
