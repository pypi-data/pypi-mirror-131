#!/usr/bin/env python3

"""
** Processes requests. **
-------------------------

Whether it is a client or a server that asks for something, it doesn't change much.
In all cases it is TCP sockets that request and render services.
That's why once the communication is established,
clients and servers use the same function to communicate.
"""

import threading

from raisin.encapsulation.packaging import Argument, Func, Task, Result
from raisin.communication.request import send_result


__pdoc__ = {
    'Handler.__enter__': True,
    'Handler.__exit__': True
}


class Handler(threading.Thread):
    """
    ** Helps a socket to communicate. **

    Attributes
    ----------
    conn : raisin.communication.abstraction.AbstractConn
        The abstract connection that allows communication.
    """

    def __init__(self, conn):
        """
        Parameters
        ----------
        conn : raisin.communication.abstraction.AbstractConn
            An entity able to communicate.
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self.conn = conn

        self._args = {}
        self._func = {}

    def run(self):
        """
        ** Wait for the requests to answer them. **

        This method must be launched asynchronously by invoking the *start* method.
        It listens for the arrival of a request through the 'conn' attribute.
        As soon as a request arrives, it is processed. Once the request is processed,
        this method starts listening for the next request.
        """
        while True:
            try:
                ask, context = self.conn.recv_formatted(
                    kind={'request', 'package'},
                    get_context=True)
            except ConnectionError:
                break

            if ask == 'hello':
                self.conn.send_formatted('hello', kind='answer', signature=context.signature)
            elif isinstance(ask, Argument):
                self._args[ask.__hash__()] = ask
            elif isinstance(ask, Func):
                self._func[ask.__hash__()] = ask
            elif isinstance(ask, Task):
                # TODO : s'assurer qu'il y ai les arguments et la fonction dispo
                func = self._func[ask.func_hash]
                args = [self._args[arg_hash].get_value() for arg_hash in ask.arg_hashes]
                # TODO : calculer le resultat dans un autre processus
                res = Result(func(*args))
                send_result(self.conn, res)

            else:
                raise NotImplementedError(f"impossible to process {ask}, it's not coded")

    def handler_close(self):
        """
        ** Clean up the connection. **
        """
        self.conn.close()

    def __del__(self):
        """
        ** Help for the garage-collector. **
        """
        self.handler_close()

    def __enter__(self):
        """
        ** Allows to manage the closure through a context manager. **
        """
        return self

    def __exit__(self, exc_type, value, traceback):
        """
        ** Guaranteed that the connection closes in all cases. **
        """
        self.handler_close()
