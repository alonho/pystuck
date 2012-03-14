import sys

def ishell():
    try:
        from IPython import embed
        embed(user_ns=sys._getframe(1).f_locals)
    except ImportError: 
        # IPython < 0.11 
        # Explicitly pass an empty list as arguments, because otherwise 
        # IPython would use sys.argv from this script. 
        try: 
            from IPython.Shell import IPShellEmbed
            ipshell = IPShellEmbed(argv=[], user_ns=sys._getframe(1).f_locals)
            ipshell()
        except ImportError: 
            # IPython not found at all, raise ImportError 
            raise 
