from urllib3.poolmanager import PoolManager as _PoolManager

import requezts


class PoolManager(_PoolManager):
    """Requests PoolManager that uses libzt sockets"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool_classes_by_scheme = {
            'http': requezts.HTTPConnectionPool,
            # TODO: add HTTPS
        }
