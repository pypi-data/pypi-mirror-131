#!/usr/bin/env python3

"""
** Allows for extensive testing around communication. **
--------------------------------------------------------
"""

import socket
import threading
import time
import uuid

import pytest

from raisin.communication.abstraction import SocketConn
from raisin.communication.server import Server
from raisin.communication.client import Client
from raisin.communication.request import hello


def test_socket_abstraction_conn():
    """
    ** Tests all fonctions of the abstraction. **
    """
    socket1, socket2 = socket.socketpair()
    abstraction1, abstraction2 = SocketConn(socket1), SocketConn(socket2)

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

def test_formatted():
    """
    ** Verifies that the threads do not mix up the packages. **
    """
    def send_and_recv(conn1, conn2):
        """ Designed to be executed multiple times from multiple threads. """
        for _ in range(10):
            signature = uuid.uuid4().bytes
            content = uuid.uuid4().bytes
            conn1.send_formatted(content, kind='answer', signature=signature)
            assert conn2.recv_formatted(signature=signature) == content

    socket1, socket2 = socket.socketpair()
    with SocketConn(socket1) as conn1, SocketConn(socket2) as conn2:
        threads = [threading.Thread(target=send_and_recv, args=(conn1, conn2)) for _ in range(16)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

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
            hello(client)
