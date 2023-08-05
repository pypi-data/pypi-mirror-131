#!/usr/bin/env python3

"""
** Allows for extensive testing around communication. **
--------------------------------------------------------
"""

import socket
import time

import pytest

from raisin.communication.abstraction import SocketAbstractConn
from raisin.communication.server import Server
from raisin.communication.client import Client
from raisin.communication.request import send_hello


def test_socket_abstraction_conn():
    """
    ** Tests all fonctions of the abstraction. **
    """
    socket1, socket2 = socket.socketpair()
    abstraction1, abstraction2 = SocketAbstractConn(socket1), SocketAbstractConn(socket2)

    abstraction1.send((b'mes', b'sage1',))
    abstraction2.send((b'hello',))
    abstraction2.send((b'',))
    abstraction1.send((b'message2',))
    assert b''.join(abstraction2.recv()) == b'message1'
    assert b''.join(abstraction2.recv()) == b'message2'
    assert b''.join(abstraction1.recv()) == b'hello'
    assert b''.join(abstraction1.recv()) == b''

    abstraction1.send_obj(0)
    abstraction1.send_obj(1)
    abstraction2.send_obj(2)
    abstraction2.send_obj(3)
    assert abstraction1.recv_obj() == 2
    assert abstraction1.recv_obj() == 3
    assert abstraction2.recv_obj() == 0
    assert abstraction2.recv_obj() == 1

    abstraction1.close()
    abstraction2.close()

@pytest.mark.slow
def test_simple_server():
    """
    ** Tries to launch a simple server. **
    """
    with Server(9999) as server:
        server.start() # the server is listening
        time.sleep(2)
        server.shutdown() # stops the server

@pytest.mark.slow
def test_simple_client():
    """
    ** Tries to lunch a simple client. **
    """
    with Server(9999) as server:
        server.start()
        time.sleep(2)
        with Client(None, 9999) as client:
            client.start()
            time.sleep(2)

@pytest.mark.slow
def test_client_interface():
    """
    ** Performs several tests on the client interface. **
    """
    with Server(9999) as server:
        server.start()
        time.sleep(2)
        with Client(None, 9999) as client:
            send_hello(client)
