from itertools import chain
from threading import enumerate as enum_threads
from traceback import format_stack
from sys import _current_frames
from .greenlets import greenlet_frame_generator

def thread_frame_generator():
    frames = _current_frames()
    for thread_ in enum_threads():
        try:
            frame = frames[thread_.ident]
        except KeyError:
            pass # race prone, threads might finish..
        else:
            yield (thread_, frame)

def pretty_format_stack(frame):
    if frame is None:
        return 'no frame found! greenlet probably ended.\n'
    return ''.join(format_stack(frame))

def stacks_repr_generator(threads=True, greenlets=True):
    for thread, frame in chain(thread_frame_generator() if threads else (),
                               greenlet_frame_generator() if greenlets else ()):
        yield "{0}\n{1}".format(thread, pretty_format_stack(frame))

def stacks_repr(*a, **k):
    return '\n'.join(stacks_repr_generator(*a, **k))

def probe(*a, **k):
    for stack in stacks_repr_generator(*a, **k):
        print (stack)
