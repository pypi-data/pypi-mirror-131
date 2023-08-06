import time
from typing import Optional

import requests
from libzt import ZeroTierNode

from requezts import _HTTPAdapter


class Session(requests.Session):
    """|  Context manager class built on ``requests.sessions.Session`` that uses libzt sockets. Manages:
    |  - ZeroTier node state
    |  - Cookie persistence
    |  - Connection pooling
    |  - Configuration

    **Note**: Due to current limitations of libzt, requezts can only manage one ZeroTier network node per process.

    :param net_id: ZeroTier network ID (64-bit unsigned integer, e.g. 0x0123456789abcdef)
    :param node_path: (optional) Path in filesystem of node configuration (will be created if not already existing)
    """

    def __init__(self, net_id: int, node_path: Optional[str] = None):

        # Initialize requests.Session. Will mount default HTTP/HTTPS adapter.
        super().__init__()

        self.__net_id = net_id
        self.__node_path = node_path

        self.__node: Optional[ZeroTierNode] = None

        # noinspection HttpUrlsUsage,PyProtectedMember
        self.mount('http://', _HTTPAdapter())
        # noinspection PyTypeChecker,PyProtectedMember
        self.mount('https://', _HTTPAdapter())  # TODO

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self) -> None:
        """
        Connect to ZeroTier network and bring node online.
        """

        assert not self.is_open(), "session already active"

        # Initialize node
        node = ZeroTierNode()
        if self.__node_path is not None:
            node.init_from_storage(self.__node_path)

        # Bring node online
        node.node_start()
        while not node.node_is_online():
            time.sleep(0.02)

        # Join the net
        node.net_join(self.__net_id)
        while not node.net_transport_is_ready(self.__net_id):
            time.sleep(0.02)

        # TODO: Allow configurable IP address

        self.__node = node

    def close(self) -> None:
        """
        Disconnect from ZeroTier network and bring node offline.
        """

        super().close()  # Call close() on all adapters

        assert self.is_open(), "session already closed"

        node = self.__node
        self.__node = None

        # Bring node down
        node.node_stop()
        node.node_free()

    def is_open(self) -> bool:
        """
        Check if Session is open (connected to ZeroTier network).

        :rtype: bool
        """
        return self.__node is not None
