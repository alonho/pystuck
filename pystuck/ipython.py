import sys

def ishell():
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed(argv=[], user_ns=sys._getframe(1).f_locals)
    ipshell()
