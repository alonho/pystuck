=======
pystuck
=======

pystuck.py is a utility for analyzing stuck python programs (or just hardcore debugging).

========
Examples
========

what is python doing?!
======================

test.py is stuck, wouldn't you just die to know where?

::
    import pystuck; pystuck.run_server().

    while True:
        with lock: # could block
             sock.recv(1024) # could block
  
running pystuck from the shell shows interesting stuff:

::
    
    % pystuck
    <_MainThread(MainThread, started -1215396160)>
      File "test.py", line 9, in <module>
        with lock: # could block

it actually prints two more threads that are related to pystuck, ignore them.

whose got the lock?!
====================

::
    # it seldom happens that a thread doesn't release the lock or stuck while holding it.
    # we want to know which thread... RLock._RLock__owner will reveal it, bare with me now.
    rlock.acquire() 

invoking pystuck again:

::
  
    % pystuck
    <_MainThread(MainThread, started -1215396160)>
      File "test.py", line 9, in <module>
        with lock: # could block
    
    <Thread(Thread-1, started -1219450000)>
      File "test.py", line 12, in <module>
        do_math()
  
    <Thread(Thread-2, started -1219540000)>
      File "test.py", line 14, in <module>
        foo()
      File "test.py", line 20, in foo
        do_network()

    In [0]: modules['sys']._current_frames() # gets a mapping between a thread to its frame (top of stack)
    Out[0]: {-1215396160: <frame object at 0x8a07154>, 
             -1219450000: <frame object at 0x8a29154>,
             -1219540000: <frame object at 0x8b39154>}
             
    In [1]: _[-1215396160] # get the stuck thread's frame
    Out[1]: <frame object at 0x8a07154> 
    
    In [2]: _.f_locals
    Out[2]: {'lock': <_RLock owner=-1219540000 count=1>}

    In [3]: # our stuck thread is probably waiting for thread 1219450000 to finish do_math.. figures

=====
usage
=====

:: 

   usage: pystuck [-h] [--no-stacks] [--no-ipython] [host] [port]

   pystuck.py is a utility for analyzing stuck python programs (or just hardcore debugging).

   in order to debug a python program (hence, the debugee),
   add this line anywhere at startup: import pystuck; pystuck.run_server().

   this script is the client, once invoked it connects to the debuggee
   and prints the debugee's threads stack traces (good for most cases).
   in addition, it opens an ipython prompt with an rpyc connection that provides
   access to the debuggee's modules (good for inspecting variables).
   positional arguments:

     host          server address (default: 127.0.0.1)
     port          server port (default: 6666)

   optional arguments:
     -h, --help    show this help message and exit
     --no-stacks   don't print the debugee's threads and stacks
     --no-ipython  don't open an ipython prompt for debugging
