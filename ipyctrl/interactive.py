from IPython.core.interactiveshell import InteractiveShell, InteractiveShellABC

class IPyCtrlInteractiveShell(InteractiveShell):
    def _showtraceback(self, etype, evalue, stb: str):
        # return super()._showtraceback(etype, evalue, stb)
        pass

InteractiveShellABC.register(IPyCtrlInteractiveShell)
