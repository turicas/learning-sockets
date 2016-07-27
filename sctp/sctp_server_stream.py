#!/usr/bin/env python3
# coding: utf-8

# Created by Álvaro Justen <https://github.com/turicas>

import socket


server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM,
                       socket.IPPROTO_SCTP)
server.bind(('127.0.0.1', 1234))
server.listen(5)

print('Waiting for a connection...', end='')
client, address = server.accept()
print('Accepted connection from {}.'.format(address))

# Since the client will send two messages, we need to `client.recv` calls here
# to read them -- on TCP, if the messages were sent fast enough, we would need
# only one call but won't be able to distinguish the messages since only one
# bytes object would be returned.

# WARNING: you should define a maximum message size for your application and
# use this value on `recv`; if not, you're going to read partial messages and
# won't know if they're partial or not. More about it on
# <http://stackoverflow.com/a/2862176/1299446>. You can also set the maximum
# socket buffers (send and receive) by using `.setsockopt` to the maximum
# message size you want (an exception will be raised if the application tries
# to send/receive more data than the maximum), but be aware of Linux doubling
# the max sizes: <http://stackoverflow.com/a/2031987/1299446>.

print('Waiting for 2 messages...')
message = client.recv(4096)  # will block until a message arrives
print('Message 1 received ({} bytes): {}'.format(len(message), message))
message = client.recv(4096)
print('Message 2 received ({} bytes): {}'.format(len(message), message))

# We're sending two messages so the client will need two `.recv` calls to read
# them all.
message = b'this is the first reply.'
bytes_sent = client.send(message)
print('Sent {} bytes: {}'.format(bytes_sent, message[:bytes_sent]))
message = b'this is the second reply.'
bytes_sent = client.send(message)
print('Sent {} bytes: {}'.format(bytes_sent, message[:bytes_sent]))

client.close()
server.close()
