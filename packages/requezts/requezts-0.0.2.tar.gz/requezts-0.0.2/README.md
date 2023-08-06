# requezts

HTTP client over encrypted P2P sockets using [ZeroTier](https://www.zerotier.com/)

**requezts** is built on Kenneth Reitz's [requests](https://github.com/psf/requests) library, and mirrors its simple and powerful interface:

    import requezts

    with requezts.Session(net_id=0x0123456789abcdef) as session:
        response = session.get("http://10.144.174.53:8000/index.html")

Using **requezts'** ``Session`` object as a context manager, you can easily establish connectivity to a ZeroTier network, while also receiving all the benefits of the underlying ``requests.session.Session`` (cookie persistence, connection pooling, and configuration).

Installation
------------------------------------

    pip install requezts

Documentation
------------------------------------

See documentation on [ReadTheDocs](https://requezts.readthedocs.io/en/latest/).

Contributions
------------------------------------

This project is open-source and contributions are welcome. The **requezts** library is hosted on [GitLab](https://gitlab.com/bostonwalker/requezts).
