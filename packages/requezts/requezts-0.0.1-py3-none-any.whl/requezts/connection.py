from typing import Optional

from urllib3.connection import HTTPConnection as _HTTPConnection
from urllib3.exceptions import LocationParseError
import libzt

import requezts


class HTTPConnection(_HTTPConnection):
    """HTTPConnection using libzt sockets"""

    def _new_conn(self):
        """Establish a new socket/connection"""

        host = self._dns_host
        if host.startswith("["):
            host = host.strip("[]")
        try:
            host.encode("idna")
        except UnicodeError:
            raise LocationParseError(f"'{host}', label empty or too long") from None

        port = self.port

        addr_info = self.getaddrinfo(host, port, family=libzt.ZTS_AF_INET, type=libzt.ZTS_SOCK_STREAM)
        if len(addr_info) == 0:
            raise OSError('getaddrinfo returns an empty list')

        while True:
            af, socktype, proto, canonname, sa = addr_info.pop()

            sock: Optional[requezts.socket] = None
            try:
                sock = requezts.socket(af, socktype, proto)

                # If provided, set socket level options before connecting
                if self.socket_options is not None:
                    for opt in self.socket_options:
                        sock.setsockopt(*opt)

                # sock.settimeout(self.timeout)  # TODO - not supported by libzt yet

                if self.source_address is not None:
                    sock.bind(self.source_address)

                sock.connect(sa)
                return sock

            except OSError as e:
                if sock is not None:
                    sock.close()
                if len(addr_info) > 0:
                    # Try another address
                    continue
                else:
                    raise e

    @staticmethod
    def getaddrinfo(host: str, port: int, family: int = 0, type: int = 0, proto: int = 0, flags: int = 0):
        """Return necessary arguments for creating sockets to each specified host
        (can be multiple in comma-separated list)"""
        # TODO
        af = libzt.ZTS_AF_INET
        socktype = libzt.ZTS_SOCK_STREAM
        proto = 0
        canonname = None
        sa = (host, port)

        return [(af, socktype, proto, canonname, sa)]
