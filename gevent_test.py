import pystuck


pystuck.run_server()

import gevent
def foo():
    gevent.sleep(1)
def foo2():
    pass


gevent.spawn(foo)
gevent.spawn(foo)
gevent.spawn(foo)
gevent.sleep(0.4)
gevent.spawn(foo2)
pystuck.run_client()
