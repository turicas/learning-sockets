#!/usr/bin/env python3
# coding: utf-8

# Created by Álvaro Justen <https://github.com/turicas>

import socket


client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM,
                       socket.IPPROTO_SCTP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)
client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
client.connect(('127.0.0.1', 1234))
print(client.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF))
print(client.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF))

message = b'this is the first message.'
bytes_sent = client.send(message)
print('Sent {} bytes: {}'.format(bytes_sent, message[:bytes_sent]))

message = b'this is the second message.'
bytes_sent = client.send(message)
print('Sent {} bytes: {}'.format(bytes_sent, message[:bytes_sent]))

print('Waiting for 2 messages...')
message = client.recv(4096)
print('Message 1 received ({} bytes): {}'.format(len(message), message))
message = client.recv(4096)
print('Message 2 received ({} bytes): {}'.format(len(message), message))

#client.close()
