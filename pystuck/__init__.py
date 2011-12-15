import socket
from pystuck.rpyc_tools import run_server, connect, DEFAULT_HOST, DEFAULT_PORT

README = """
pystuck.py is a utility for analyzing stuck python programs (or just hardcore debugging).

in order to debug a python program (hence, the debugee),
add this line anywhere at startup: import pystuck; pystuck.run_server().

this script is the client, once invoked it connects to the debuggee
and prints the debugee's threads stack traces (good for most cases).
in addition, it opens an ipython prompt with an rpyc connection that provides
access to the debuggee's modules (good for inspecting variables)."""

def run_client(host=DEFAULT_HOST, port=DEFAULT_PORT, print_stacks=True, ipython=True):
    conn = connect(host=host, port=port)
    if print_stacks:
        print conn.modules['pystuck.thread_probe'].stacks_repr()
    if ipython:
        from pystuck.ipython import ishell
        modules = conn.modules
        print "use the 'modules' dictionary to access remote modules (like 'os', or '__main__')"
        ishell()

def main():
    import argparse

    parser = argparse.ArgumentParser(description=README)
    parser.add_argument('host', nargs='?', default=DEFAULT_HOST, help='server address (default: {})'.format(DEFAULT_HOST))
    parser.add_argument('port', nargs='?', default=DEFAULT_PORT, help='server port (default: {})'.format(DEFAULT_PORT))
    parser.add_argument('--no-stacks', action='store_false', dest='stacks', help="don't print the debugee's threads and stacks")
    parser.add_argument('--no-ipython', action='store_false', dest='ipython', help="don't open an ipython prompt for debugging")
    args = parser.parse_args()

    try:
        run_client(host=args.host, port=args.port, print_stacks=args.stacks, ipython=args.ipython)
    except socket.error:
        print "unable to connect to the server, please follow the instructions:"
        print README

if __name__ == '__main__':
    main()
