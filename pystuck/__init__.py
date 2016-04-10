"""
pystuck is a utility for analyzing stuck python programs (or just hardcore
debugging).

In order to debug a python program (hence, the debugee),
add this line anywhere at startup: import pystuck; pystuck.run_server().

This script is the client, once invoked it connects to the debuggee
and prints the debugee's threads stack traces (good for most cases).
In addition, it opens an ipython prompt with an rpyc connection that provides
access to the debuggee's modules (good for inspecting variables).
"""
import socket
from pystuck.rpyc_tools import run_server, DEFAULT_HOST, DEFAULT_PORT


def run_client(host=DEFAULT_HOST, port=DEFAULT_PORT, stacks=False, ipython=True,
               greenlets=True):
    from rpyc.utils.classic import connect
    conn = connect(host=host, port=port)
    if stacks:
        print(conn.modules['pystuck.thread_probe'].stacks_repr(
            greenlets=greenlets))
    if ipython:
        from pystuck.ipython import ishell
        modules = conn.modules
        ishell(local_ns=locals())


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '--host', default=DEFAULT_HOST,
        help='server address (default: {0})'.format(DEFAULT_HOST)
    )
    parser.add_argument(
        '--port', default=DEFAULT_PORT, type=int,
        help='server port (default: {0})'.format(DEFAULT_PORT)
    )
    parser.add_argument(
        '--stacks', action='store_true', dest='stacks',
        help="Print all thread/greenlet stack traces on initial shell entry"
    )
    parser.add_argument(
        '--exclude-greenlets', action='store_false',
        dest='greenlets', help="don't print the debugee's greenlets. pass it "
        "when the process hogs memory as printing greenlets requires traversal"
        " of all objects in the garbage collector")
    parser.add_argument(
        '--no-ipython', action='store_false', dest='ipython',
        help="don't open an ipython prompt for debugging"
    )
    args = parser.parse_args()

    if not args.ipython:
        # if no shell then just print the bts
        args.stacks = True
        print("Printing all thread backtraces:\n")

    try:
        run_client(**vars(args))
    except socket.error:
        print("unable to connect to the server, please follow the "
              "instructions:")
        print(__doc__)

if __name__ == '__main__':
    main()
