from itertools import chain
from threading import enumerate as enum_threads
from traceback import format_stack
from sys import _current_frames
import gc

def thread_frame_generator():
    frames = _current_frames()
    for thread_ in enum_threads():
        try:
            frame = frames[thread_.ident]
        except KeyError:
            pass # race prone, threads might finish..
        else:
            yield (thread_, frame)

# the greenlet iteration concept is copied from:
# https://github.com/mozilla-services/powerhose/blob/master/powerhose/util.py#L200
# thanks Tarek!
def greenlet_frame_generator():
    try:
        from greenlet import greenlet
    except ImportError:
        return
    for ob in gc.get_objects():
        if not isinstance(ob, greenlet):
            continue
        if not ob:
            continue # not running anymore or not started
        yield ob, ob.gr_frame

def pretty_format_stack(frame):
    return ''.join(format_stack(frame))
    
def stacks_repr_generator(threads=True, greenlets=True):
    for thread, frame in chain(thread_frame_generator() if threads else (),
                               greenlet_frame_generator() if greenlets else ()):
        yield "{}\n{}".format(thread, pretty_format_stack(frame))

def stacks_repr(*a, **k):
    return '\n'.join(stacks_repr_generator(*a, **k))
        
def probe(*a, **k):
    for stack in stacks_repr_generator(*a, **k):
        print stack
