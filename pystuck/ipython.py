"""
IPython shell wrapping
"""
from IPython.core.magic import (Magics, magics_class, line_magic)


def ishell(local_ns):
    """Embed an IPython shell handing it the local namespace from
    :var:`local_ns`.
    """
    banner = (
        "Welcome to the pystuck interactive shell.\nUse the 'modules' dictionary "
        "to access remote modules (like 'os', or '__main__')\nUse the `%show "
        "threads` magic to display all thread stack traces.\n"
    )
    try:
        from IPython.terminal.embed import InteractiveShellEmbed
        ipshell = InteractiveShellEmbed(
            banner1=banner)
        ipshell.register_magics(IntrospectMagics)
        ipshell(local_ns=local_ns)
    except ImportError:
        # IPython < 0.11
        # Explicitly pass an empty list as arguments, because otherwise
        # IPython would use sys.argv from this script.
        try:
            from IPython.Shell import IPShellEmbed
            ipshell = IPShellEmbed(argv=[], user_ns=local_ns, banner1=banner)
            ipshell.register_magics(IntrospectMagics)
            ipshell()
        except ImportError:
            # IPython not found at all, raise ImportError
            raise


@magics_class
class IntrospectMagics(Magics):
    """Custom magics for thread inspection
    """
    @property
    def modules(self):
        '''Return the rpyc module namespace
        '''
        ns = self.shell.user_ns
        return ns['modules']

    @line_magic
    def show(self, line):
        """Show stack trace information from the remote Python process.
        More subcommands are expected to be added in the near future.

        Usage:

            show threads : Print all thread backtraces to the console
        """
        if line == 'threads':
            print(self.modules['pystuck.thread_probe'].stacks_repr())
