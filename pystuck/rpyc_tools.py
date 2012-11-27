from rpyc.utils.server import ThreadedServer
from rpyc.core import SlaveService
import threading
import os

DEFAULT_PORT = 6666
DEFAULT_HOST = "127.0.0.1"

def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT, unix_socket=None):
    args = dict(hostname=host, port=port) if unix_socket is None else dict(socket_path=unix_socket)
    if unix_socket is not None:
        try:
            os.unlink(unix_socket)
        except OSError:
            pass
    server = ThreadedServer(service=SlaveService,
                            auto_register=False,
                            **args)
    thread = threading.Thread(target=server.start)
    thread.daemon = True
    thread.start()
