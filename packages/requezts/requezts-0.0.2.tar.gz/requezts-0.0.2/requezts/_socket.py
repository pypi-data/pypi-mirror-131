import io
import socket
from typing import Optional, Union

import libzt


# noinspection PyPep8Naming
class _socket(libzt.sockets.socket):
    """Wrapper over libzt socket

    Internal object to requezts. Should not be called by user code.
    """

    def __init__(self, sock_family=-1, sock_type=-1, sock_proto=-1, sock_fd=None):
        super().__init__(sock_family, sock_type, sock_proto, sock_fd)

    def has_dualstack_ipv6(self):
        return super().has_dualstack_ipv6()

    @property
    def family(self):
        return super().family()

    @property
    def type(self):
        return super().type()

    @property
    def proto(self):
        return super().proto()

    def create_connection(self, remote_address):
        return super().create_connection(remote_address)

    def create_server(self, local_address, sock_family=libzt.ZTS_AF_INET, backlog=None):
        return super().create_server(local_address, sock_family, backlog)

    def accept(self):
        return super().accept()

    def bind(self, local_address):
        super().bind(local_address)

    def close(self):
        super().close()

    def connect(self, address):
        super().connect(address)

    def connect_ex(self, address):
        return super().connect_ex(address)

    def fileno(self):
        return super().fileno()

    def get_inheritable(self):
        return super().get_inheritable()

    def getblocking(self):
        return super().getblocking()

    def getsockopt(self, level, optname, buflen=None):
        return super().getsockopt(level, optname, buflen)

    def ioctl(self, request, arg=0, mutate_flag=True):
        return super().ioctl(request, arg, mutate_flag)

    def listen(self, backlog=None):
        super().listen(backlog)

    # noinspection PyMethodOverriding
    def makefile(self, mode: Optional[str] = None, buffering: Optional[int] = None, *, encoding: Optional[str] = None,
                 errors: Optional[str] = None, newline: Optional[str] = None) -> io.IOBase:
        """Return an IO object connected to the socket
        Modeled after cpython implementation: https://github.com/python/cpython/blob/main/Lib/socket.py

        :param mode: (optional) File mode (one of ["r", "w", "rw", "rb", "wb", "rwb"], default: "r")
        :param buffering: (optional) Buffer size:
            If positive, will return buffered io object with buffer size = `buffering`.
            If zero, will return unbuffered io object.
            If negative or `None`, will default to io.DEFAULT_BUFFER_SIZE.
        :param encoding: (optional) Text encoding
        :param errors: (optional) Specifies how encoding and decoding errors are handled by io.TextIOWrapper object.
        :param newline: (optional) Specifies how newlines are handled by io.TextIOWrapper object.
        """
        mode = mode or "r"
        if mode not in ["r", "w", "rw", "rb", "wb", "rwb"]:
            raise ValueError(f"Invalid mode: \"{mode}\"")

        if (buffering is None) or (buffering < 0):
            buffering = io.DEFAULT_BUFFER_SIZE

        encoding = encoding or "locale"  # TODO: use io.text_encoding() helper func (available in Python 3.10+)

        reading = "r" in mode
        writing = "w" in mode
        binary = "b" in mode

        if (buffering == 0) and (not binary):
            raise ValueError("Unbuffered streams must be binary")

        raw_mode = ("r" if reading else "") + ("w" if writing else "")  # Remove "b"

        res = _SocketIO(self, raw_mode)

        if buffering > 0:
            # Wrap in buffer object
            if reading and writing:
                res = io.BufferedRWPair(res, res, buffer_size=buffering)
            elif reading:
                res = io.BufferedReader(res, buffer_size=buffering)
            else:
                assert writing
                res = io.BufferedWriter(res, buffer_size=buffering)

            if not binary:
                # Wrap in encoding object
                res = io.TextIOWrapper(res, encoding=encoding, errors=errors, newline=newline)
                # noinspection PyPropertyAccess
                res.mode = mode

        return res

    def recv(self, n_bytes, flags=0):
        return super().recv(n_bytes, flags)

    def recv_into(self, buffer: Union[bytearray, memoryview], n_bytes: int = 0, flags: int = 0) -> int:
        """Read received data into buffer
        Based on cpython implementation: socketmodule.c::sock_recv_into()

        :param buffer: Byte buffer
        :param n_bytes: (optional) Number of bytes to read (default: length of buffer)
        :param flags: (optional) Flags
        :return: Number of bytes read
        """
        if n_bytes < 0:
            raise ValueError("negative buffersize in recv_into")

        n_bytes = n_bytes or len(buffer)

        if len(buffer) < n_bytes:
            raise ValueError("buffer too small for requested bytes")

        if n_bytes > 0:
            # TODO: Bypass recv() and implement this at the native level
            recv_bytes = self.recv(n_bytes, flags=flags)
            n_bytes_recv = len(recv_bytes)
            buffer[:n_bytes_recv] = recv_bytes
            return n_bytes_recv
        else:
            return 0

    def send(self, data, flags=0):
        return super().send(data, flags)

    def sendall(self, data: Union[bytes, bytearray, memoryview], flags: int = 0) -> None:
        """Send all data
        https://stackoverflow.com/questions/34252273/what-is-the-difference-between-socket-send-and-socket-sendall
        """
        while True:
            bytes_sent: int = self.send(data, flags=flags)
            if bytes_sent > 0:
                data = data[bytes_sent:]
                continue
            else:
                break

    def setblocking(self, flag):
        super().setblocking(flag)

    def setsockopt(self, level, optname, value):
        super().setsockopt(level, optname, value)

    def settimeout(self, value):
        # TODO
        pass

    def shutdown(self, how):
        super().shutdown(how)


class _SocketIO(socket.SocketIO):
    """IO implementation on top of libzt sockets

    Internal object to requezts. Should not be called by user code.

    :param sock: requezts Socket
    :param mode: File mode (one of ["r", "w", "rw", "rb", "wb", "rwb"])
    """

    def __init__(self, sock: _socket, mode: str):
        # noinspection PyTypeChecker
        super().__init__(sock, mode)

    def close(self) -> None:
        """Close the SocketIO object"""
        if not self.closed:
            io.RawIOBase.close(self)  # Call super() (bypass socket.SocketIO.close())
            # noinspection PyAttributeOutsideInit
            self._sock = None
