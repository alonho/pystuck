import greenlets
import threading
import os

DEFAULT_PORT = 6666
DEFAULT_HOST = "127.0.0.1"

def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT, unix_socket=None, patch_greenlet=True):
    if patch_greenlet and greenlets.greenlet_available:
        greenlets.patch()

    args = dict(hostname=host, port=port) if unix_socket is None else dict(socket_path=unix_socket)
    if unix_socket is not None:
        try:
            os.unlink(unix_socket)
        except OSError:
            pass

    # lazy imports make pystuck cooperative with gevent.
    # users can import pystuck and gevent in any order.
    # users should patch before calling run_server in order for rpyc to be patched.
    from rpyc.utils.server import ThreadedServer
    from rpyc.core import SlaveService
    server = ThreadedServer(service=SlaveService,
                            auto_register=False,
                            **args)
    thread = threading.Thread(target=server.start)
    thread.daemon = True
    thread.start()
