from threading import enumerate as enum_threads
from traceback import format_stack
from sys import _current_frames

def thread_and_stack_generator():
    frames = _current_frames()
    for thread_ in enum_threads():
        try:
            frame = frames[thread_.ident]
            stack_list = format_stack(frame)
            yield (thread_, ''.join(stack_list))
        except KeyError:
            pass # race prone, threads might finish..

def stacks_repr():
    return '\n'.join("{}\n{}".format(thread, stack)
                     for thread, stack in thread_and_stack_generator())    

def probe():
    print stacks_repr()
