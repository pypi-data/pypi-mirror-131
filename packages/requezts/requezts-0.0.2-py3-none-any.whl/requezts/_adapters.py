import requests

from requezts._poolmanager import _PoolManager


# noinspection PyUnresolvedReferences
class _HTTPAdapter(requests.adapters.HTTPAdapter):
    """requests HTTPAdapter using libzt sockets

    Internal object to requezts. Should not be called by user code.
    """

    def init_poolmanager(self, connections, maxsize, block=..., **pool_kwargs):
        """Initializes a urllib3 PoolManager.
        This method should not be called from user code, and is only
        exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.
        :param connections: The number of urllib3 connection pools to cache.
        :param maxsize: The maximum number of connections to save in the pool.
        :param block: Block when no free connections are available.
        :param pool_kwargs: Extra keyword arguments used to initialize the Pool Manager.
        """
        # save these values for pickling
        self._pool_connections = connections
        self._pool_maxsize = maxsize
        self._pool_block = block

        self.poolmanager = _PoolManager(num_pools=connections, maxsize=maxsize, block=block, strict=True,
                                        **pool_kwargs)
