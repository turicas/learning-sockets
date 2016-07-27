# SCTP

This repository shows simple [SCTP][sctp] usage in Python3.

[SCTP (Stream Control Transmission Protocol)][sctp] is a transport-layer
protocol (same layer of UDP and TCP); it is message-oriented (like UDP, unlike
TCP) but is reliable and guarantees order (like TCP, unlike UDP). See all [SCTP
features][features]. The protocol is defined by [RFC4960][rfc4960] (an
introduction is provided by [RFC3286][rfc3286]). Read more about it on
[sctp.be][sctpbe].


## Installing Dependencies

    apt-get install libsctp1 libsctp-dev lksctp-tools


## Modes of Operation

[SCTP][sctp] can be used either with socket type `SOCK_STREAM` (like TCP) or
either via `SOCK_SEQPACKET`. The fastest way of translating a TCP application
to SCTP is to use `SOCK_STREAM` since the system calls (low level socket API)
will be the same, you just need to pass the `socket.IPPROTO_SCTP` parameter to
the `socket.socket` class; it's also the simpler method of using SCTP since
you're going to receive the whole message on each `recv` call.

Two client/server examples are available on this repository showing the
differences between the system calls:

- `SOCK_STREAM`: `sctp_server_stream.py` and `sctp_client_stream.py`
- `SOCK_SEQPACKET`: `sctp_server_seqpacket.py` and `sctp_client_seqpacket.py`

> **Tip**: see comments on server files.


### Note on `SOCK_STREAM` Meaning

Despite the type `SOCK_STREAM`, the [SCTP][sctp] socket won't be an "infinite
stream of data" like TCP, because **it's message-oriented**.

Let's illustrate with an example: a client send two messages to a server.

- First scenario: TCP (`socket.socket(AF_INET, SOCK_STREAM)`). If the messages
  are sent fast enough, you'll need only one `socket.recv` call on the server
  side to get the two messages -- and there will not be a boundary between
  them. This approach will make possible the case where you need to call
  `socket.recv` many times to receive only "one message", depending on network
  buffers.
- Second scenario: SCTP as `SOCK_STREAM` (`socket.socket(AF_INET, SOCK_STREAM,
  IPPROTO_SCTP)`). Event if the messages are sent fast enough, you'll need two
  `socket.recv` calls on the server side to get the two messages -- and there
  is no way of getting them with just one system call.

> **WARNING**: if using `SOCK_STREAM` you should define a maximum message size
> for your application and use this value on `recv`; if not, you're going to
> read partial messages and won't know if they're partial or not. More about it
> on <http://stackoverflow.com/a/2862176/1299446>. You can also set the maximum
> socket buffers (send and receive) by using `.setsockopt` to the maximum
> message size you want (an exception will be raised if the application tries
> to send/receive more data than the maximum), but be aware of Linux doubling
> the max sizes: <http://stackoverflow.com/a/2031987/1299446>.


## Using SCTP on Python2

You can use a SCTP `SOCK_STREAM` socket on Python2 by setting
`socket.IPPROTO_SCTP = 132` (as defined on `/usr/include/netinet/sctp.h`).
There's no API support for `recvmsg` and `sendmsg` needed by `SOCK_SEQPACKET`.

[features]: https://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol#Features
[rfc3286]: https://tools.ietf.org/html/rfc3286
[rfc4960]: https://tools.ietf.org/html/rfc4960
[sctp]: https://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol
[sctpbe]: http://www.sctp.be/
