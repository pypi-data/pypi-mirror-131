#!/usr/bin/env python3

"""
** Establishes small communications. **
---------------------------------------

Allows via ``raisin.communication.abstraction.AbstractConn``,
to take small requests or short exchanges.
The connection must in most cases be connected to another listening connection.
That is, indirectly connected to a ``raisin.communication.handler.Handler``.
"""

def send_hello(conn):
    """
    ** Sends a 'hello' and expects a 'hello' in return. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.AbstractConn
        A connection to a ``raisin.communication.handler.Handler``.

    Raises
    ------
    ValueError
        If the answer is not the one expected.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketAbstractConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.communication.request import send_hello
    >>>
    >>> soc1, soc2 = socket.socketpair()
    >>> hand = Handler(SocketAbstractConn(soc2))
    >>> hand.start()
    >>>
    >>> send_hello(SocketAbstractConn(soc1))
    >>>
    >>> hand.handler_close()
    >>>
    """
    conn.send_obj((b'ask', b'hello'))
    rep = conn.recv_obj()
    # TODO : verifier la reponse
    if rep != ((b'rep', b'hello')):
        raise ValueError(f'the answer is not the one expected ({rep})')
