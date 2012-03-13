=======
pystuck
=======

pystuck.py is a utility for analyzing stuck python programs (or just hardcore debugging).

pystuck currently has two major features:

1. print all running threads' stack traces.
2. remote inspection of modules and variables without interrupting the program.

in the debugged script: import pystuck; pystuck.run_server()

to invoke the client: invoke pystuck from the shell.

production use
==============

pystuck doesn't consume resources when no client is connected to it. 

all the run_server function does is spawn a thread that blocks on accept (waiting for clients to connect), so it can be used in production.


there are two drawbacks for using pystuck in production:

1. meddling with variables and modules is not thread safe.
2. a potential security breach - nothing prevents an unprivilidged user connect to a privlidged running python process and use the remote access to do practically anything.

=======
install
=======

::

    pip install pystuck

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

    ...

it's stuck waiting for the lock!.
it actually prints two more threads that are related to pystuck, ignore them.

who's got the lock?!
====================

::

    # it seldom happens that a thread doesn't release the lock or is stuck while holding it.
    # we want to know which thread... bear with me now.
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

    use the 'modules' dictionary to access remote modules (like 'os', or '__main__')

    In [0]: modules['sys']._current_frames() # gets a mapping between a thread to its frame (top of stack)
    Out[0]: {-1215396160: <frame object at 0x8a07154>, 
             -1219450000: <frame object at 0x8a29154>,
             -1219540000: <frame object at 0x8b39154>}
             
    In [1]: _[-1215396160] # get the stuck thread's frame
    Out[1]: <frame object at 0x8a07154> 
    
    In [2]: _.f_locals # local variables of the function
    Out[2]: {'lock': <_RLock owner=-1219450000 count=1>}

    In [3]: # our stuck thread is probably waiting for thread 1219450000 to finish do_math.. figures

what rpyc can do for you
========================

rpyc is the library used to communicate python objects and procedure calls across processes.
here are some of the things you can do to the already running server.

::
    
    % pystuck
    
    (stacks appear here...)
 
    In [1]: modules['sys'].stdout = file("/tmp/log.txt", "w") # tunnel the script's stdout to log
    
    In [2]: modules['__main__'].global_var = 100 # change and inspect variables in the __main__ module (the name of the script when invoked like this: python script.py)

    In [3]: socket = modules['socket'].socket() # create a socket object opened by the server script!
 
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
