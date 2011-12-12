from rpyc.utils.classic import connect as rpyc_connect
from rpyc.utils.server import ThreadedServer
from rpyc.core import SlaveService
import threading

DEFAULT_PORT = 6666
#DEFAULT_PORT = os.getpid() # multiple processes can co-exist
DEFAULT_HOST = "127.0.0.1" 
#DEFAULT_HOST = "0.0.0.0" # reachable from outside the machine (security hole!)

def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT):
    server = ThreadedServer(service=SlaveService,
                            hostname=host,
                            port=port,
                            auto_register=False)
    thread = threading.Thread(target=server.start)
    thread.daemon = True
    thread.start()
                              
def connect(host=DEFAULT_HOST, port=DEFAULT_PORT):
    return rpyc_connect(host=host, port=port)
