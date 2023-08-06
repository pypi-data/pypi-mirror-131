import urllib3

from requezts import _HTTPConnection


class _HTTPConnectionPool(urllib3.connectionpool.HTTPConnectionPool):
    """HTTPConnectionPool using libzt sockets

    Internal object to requezts. Should not be called by user code.
    """
    ConnectionCls = _HTTPConnection
