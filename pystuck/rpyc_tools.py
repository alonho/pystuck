from . import greenlets
import threading
import os

DEFAULT_PORT = 6666
DEFAULT_HOST = "127.0.0.1"

def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT, unix_socket=None, patch_greenlet=True, service_class_getter=None, **server_args):
    if patch_greenlet and greenlets.greenlet_available:
        greenlets.patch()

    args = dict(hostname=host, port=port) if unix_socket is None else dict(socket_path=unix_socket)
    if unix_socket is not None:
        try:
            os.unlink(unix_socket)
        except OSError:
            pass

    args.update(server_args)

    # lazy imports make pystuck cooperative with gevent.
    # users can import pystuck and gevent in any order.
    # users should patch before calling run_server in order for rpyc to be patched.
    from rpyc.utils.server import ThreadedServer
    from rpyc.core import SlaveService

    # Run `SlaveService` as the default service, unless we get
    # `service_class_getter`, a callable that should return a
    # `Service` class.
    # The reason `service_class_getter` is a callable is to allow
    # `run_server` to first monkey patch and only then evaluate
    # the service class. The callable should prefer lazy imports
    # as above.
    service_class = SlaveService
    if service_class_getter is not None:
        service_class = service_class_getter()

    server = ThreadedServer(service=service_class,
                            auto_register=False,
                            **args)
    thread = threading.Thread(target=server.start)
    thread.daemon = True
    thread.start()
