from urllib3.connectionpool import HTTPConnectionPool as _HTTPConnectionPool

import requezts


class HTTPConnectionPool(_HTTPConnectionPool):
    """HTTPConnectionPool using libzt sockets"""
    ConnectionCls = requezts.HTTPConnection
