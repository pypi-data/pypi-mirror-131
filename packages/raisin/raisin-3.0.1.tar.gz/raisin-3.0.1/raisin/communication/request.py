#!/usr/bin/env python3

"""
** Establishes small communications. **
---------------------------------------

Allows via ``raisin.communication.abstraction.SelectiveConn``,
to take small requests or short exchanges.
The connection must in most cases be connected to another listening connection.
That is, indirectly connected to a ``raisin.communication.handler.Handler``.
"""

def hello(conn):
    """
    ** Sends a 'hello' and expects a 'hello' in return. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.

    Raises
    ------
    ValueError
        If the answer is not the one expected.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.communication.request import hello
    >>>
    >>> soc1, soc2 = socket.socketpair()
    >>> with SocketConn(soc1) as conn, Handler(SocketConn(soc2)) as handler:
    ...     handler.start()
    ...     hello(conn)
    ...
    'hello'
    >>>
    """
    return conn.dialog('hello')

def send_package(conn, package):
    """
    ** Sends an ``raisin.encapsulation.packaging.Package``. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.
    package : raisin.encapsulation.packaging.Package
        A package that allows to contribute to the execution of a task.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.encapsulation.packaging import Argument
    >>> from raisin.communication.request import send_package
    >>>
    >>> arg = Argument(0)
    >>> soc1, soc2 = socket.socketpair()
    >>> with SocketConn(soc1) as conn, Handler(SocketConn(soc2)) as handler:
    ...     handler.start()
    ...     send_package(conn, arg)
    ...
    >>>
    """
    conn.send_formatted(package, kind='package')

def send_result(conn, result):
    """
    ** Sends an ``raisin.encapsulation.packaging.Result``. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.
    result : raisin.encapsulation.packaging.Result
        The result of the task.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.encapsulation.packaging import Result
    >>> from raisin.communication.request import send_result
    >>>
    >>> res = Result(0)
    >>> soc1, soc2 = socket.socketpair()
    >>> with SocketConn(soc1) as conn, Handler(SocketConn(soc2)) as handler:
    ...     handler.start()
    ...     send_result(conn, res)
    ...
    >>>
    """
    conn.send_formatted(result, kind='result')
