import lldb
import threading
import time
 
class UnixSignalDisabler(threading.Thread):
    def __init__(self, debugger):
        super(UnixSignalDisabler, self).__init__()
        self._debugger = debugger
        self._handled = set()
 
    def _suppress_signals(self, process):
        print("UnixSignalDisabler: disabling SIGUSR1, SIGUSR2 in process #" + str(process.GetUniqueID()))
        signals = process.GetUnixSignals()
        signals.SetShouldStop(11, False) # SIGUSR1
        signals.SetShouldStop(12, False) # SIGUSR2
 
 
    def run(self):
        while True:
            for target in self._debugger:
                if target:
                    process = target.GetProcess()
                    if process and not process.GetUniqueID() in self._handled:
                        self._suppress_signals(process)
                        self._handled.add(process.GetUniqueID())
            # Don't hog CPU
            time.sleep(0.03)
 
def __lldb_init_module(debugger, *rest):
    # Can't use 'debugger' reference directly because it gets deleted after calling '__lldb_init_module'
    debugger = lldb.SBDebugger.FindDebuggerWithID(debugger.GetID())
    listener_thread = UnixSignalDisabler(debugger)
    listener_thread.start()
