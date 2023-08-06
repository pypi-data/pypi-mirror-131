import urllib3

from requezts import _HTTPConnectionPool


class _PoolManager(urllib3.poolmanager.PoolManager):
    """Requests PoolManager that uses libzt sockets

    Internal object to requezts. Should not be called by user code."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool_classes_by_scheme = {
            'http': _HTTPConnectionPool,
            # TODO: add HTTPS
        }
