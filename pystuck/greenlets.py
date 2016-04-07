try:
    import greenlet
except ImportError:
    greenlet_available = False
else:
    greenlet_available = True
    is_patched = False

    from weakref import WeakSet

    orig_greenlet = greenlet.greenlet

    greenlets = WeakSet()

    class PatchedGreenlet(orig_greenlet):
        def __init__(self, *a, **k):
            super(PatchedGreenlet, self).__init__(*a, **k)
            greenlets.add(self)

    def patch():
        global is_patched
        is_patched = True
        greenlets.add(greenlet.getcurrent())
        greenlet.greenlet = PatchedGreenlet

    def restore():
        global is_patched
        is_patched = False
        greenlet.greenlet = orig_greenlet

# the greenlet iteration concept is copied from:
# https://github.com/mozilla-services/powerhose/blob/master/powerhose/util.py#L200
# thanks Tarek!
def greenlets_from_memory():
    import gc

    try:
        from greenlet import greenlet
    except ImportError:
        return
    for ob in gc.get_objects():
        if not isinstance(ob, greenlet):
            continue
        if not ob:
            continue # not running anymore or not started
        yield ob

def greenlet_frame_generator():
    global greenlets
    if not greenlet_available:
        return
    greenlets = greenlets if is_patched else greenlets_from_memory()
    for greenlet in greenlets:
        yield (greenlet, greenlet.gr_frame)
