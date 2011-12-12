"""
insert the following line in the debugee: import pyrobe; pyrobe.run_server()
insert the following line in the debugger: import pyrobe; pyrobe.run_client()
or just call pyrobe.py from the command line.
"""
from pyrobe.rpyc_tools import run_server, connect, DEFAULT_HOST, DEFAULT_PORT

def run_client(host=DEFAULT_HOST, port=DEFAULT_PORT, print_stacks=True, ipython=True):
    conn = connect(host=host, port=port)
    if print_stacks:
        print conn.modules['pyrobe.thread_probe'].stacks_repr()
    if ipython:
        from pyrobe.ipython import ishell
        modules = conn.modules
        print "use the 'modules' dictionary to access remote modules (like 'os', or '__main__')"
        ishell()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='pyrobe.py is a debug utility for probing and investigating running python programs, it requires the debuggee to run an integrated server by importing pyrobe and calling pyrobe.runserver()')
    parser.add_argument('host', nargs='?', default=DEFAULT_HOST, help='server address (default: {})'.format(DEFAULT_HOST))
    parser.add_argument('port', nargs='?', default=DEFAULT_PORT, help='server port (default: {})'.format(DEFAULT_PORT))
    args = parser.parse_args()

    run_client(host=args.host, port=args.port)

if __name__ == '__main__':
    main()
