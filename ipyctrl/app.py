from typing import cast
from IPython.core.shellapp import InteractiveShellApp
from IPython.core.application import BaseIPythonApplication
from traitlets import Type

from .interactive import IPyCtrlInteractiveShell

class IPyCtrlApp(BaseIPythonApplication, InteractiveShellApp):
    shell: IPyCtrlInteractiveShell

    name = 'ipyctrl'
    description = 'A programatic shell for IPython'

    def initialize(self, argv=None):
        self.init_path()
        # create the shell
        self.init_shell()
        self.init_gui_pylab()
        self.init_extensions()
        self.init_code()
        return super().initialize(argv)
    
    def init_shell(self):
        self.shell = cast(IPyCtrlInteractiveShell,
                          IPyCtrlInteractiveShell.instance(
                              parent=self,
                              profile_dir=self.profile_dir,
                              ipython_dir=self.ipython_dir, user_ns=self.user_ns
        ))
        self.shell.configurables.append(self) # type: ignore
