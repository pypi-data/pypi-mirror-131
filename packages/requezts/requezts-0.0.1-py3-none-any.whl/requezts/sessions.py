import time
from typing import Optional

import requests
from libzt import ZeroTierNode

import requezts


class Session(requests.Session):
    """Requests session that uses libzt sockets. Manages:
    - ZeroTier node state
    - Cookie persistence
    - Connection pooling
    - Configuration

    :param net_id: ZeroTier network ID (64-bit unsigned integer, e.g. 0x0123456789abcdef)
    :param node_path: (optional) Path in filesystem of node configuration (will be created if not already existing)
    """

    def __init__(self, net_id: int, node_path: Optional[str] = None):

        # Initialize requests.Session. Will mount default HTTP/HTTPS adapter.
        super().__init__()

        self.__net_id = net_id
        self.__node_path = node_path

        self.__node: Optional[ZeroTierNode] = None

        # noinspection HttpUrlsUsage
        self.mount('http://', requezts.HTTPAdapter())
        # noinspection PyTypeChecker
        self.mount('https://', requezts.HTTPAdapter())  # TODO

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self) -> None:
        """Prepare ZeroTier transport to begin facilitating connections"""

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
        """Shut down ZeroTier transport"""

        super().close()  # Call close() on all adapters

        assert self.is_open(), "session already closed"

        node = self.__node
        self.__node = None

        # Bring node down
        node.node_stop()
        node.node_free()

    def is_open(self):
        """Check if session is already open"""
        return self.__node is not None