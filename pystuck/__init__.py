import socket
from rpyc.utils.classic import connect, unix_connect
from pystuck.rpyc_tools import run_server, DEFAULT_HOST, DEFAULT_PORT

README = """
pystuck.py is a utility for analyzing stuck python programs (or just hardcore debugging).

in order to debug a python program (hence, the debugee),
add this line anywhere at startup: import pystuck; pystuck.run_server().

this script is the client, once invoked it connects to the debuggee
and prints the debugee's threads stack traces (good for most cases).
in addition, it opens an ipython prompt with an rpyc connection that provides
access to the debuggee's modules (good for inspecting variables)."""

def run_client(host=DEFAULT_HOST, port=DEFAULT_PORT, unix_socket=None, stacks=True, ipython=True, greenlets=True):
    conn = connect(host=host, port=port) if unix_socket is None else unix_connect(unix_socket)
    if stacks:
        print conn.modules['pystuck.thread_probe'].stacks_repr(greenlets=greenlets)
    if ipython:
        from pystuck.ipython import ishell
        modules = conn.modules
        print "use the 'modules' dictionary to access remote modules (like 'os', or '__main__')"
        ishell()

def main():
    import argparse

    parser = argparse.ArgumentParser(description=README)
    parser.add_argument('--host', default=DEFAULT_HOST, help='server address (default: {})'.format(DEFAULT_HOST))
    parser.add_argument('--port', default=DEFAULT_PORT, type=int, help='server port (default: {})'.format(DEFAULT_PORT))
    parser.add_argument('--unix_socket', default=None, help='server unix domain socket')
    parser.add_argument('--no-stacks', action='store_false', dest='stacks', help="don't print the debugee's threads/greenlets")
    parser.add_argument('--exclude-greenlets', action='store_false', dest='greenlets', help="don't print the debugee's greenlets. pass it when the process hogs memory as printing greenlets requires traversal of all objects in the garbage collector")
    parser.add_argument('--no-ipython', action='store_false', dest='ipython', help="don't open an ipython prompt for debugging")
    args = parser.parse_args()

    try:
        run_client(**vars(args))
    except socket.error:
        print "unable to connect to the server, please follow the instructions:"
        print README

if __name__ == '__main__':
    main()
