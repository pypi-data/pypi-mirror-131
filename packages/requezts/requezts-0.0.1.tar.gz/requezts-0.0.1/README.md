# requezts

HTTP client over encrypted p2p ZeroTier sockets, built on https://github.com/psf/requests

## Usage

    import requezts
    
    with requezts.session(net_id=0x0123456789abcdef) as session:
        response = session.get("http://10.144.174.53:8000/index.html")

