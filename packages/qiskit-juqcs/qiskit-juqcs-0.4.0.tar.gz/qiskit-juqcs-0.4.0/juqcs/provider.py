'''Provider for JUQCS backends.'''

from qiskit.providers import BaseProvider

from juqcs.backend import QasmSimulator, StatevectorSimulator

class JuqcsProvider(BaseProvider):
    '''Provider for JUQCS backends'''
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def backends(self, name=None):
        '''Return list of available backends'''
        backends = [QasmSimulator(provider=self),
                    StatevectorSimulator(provider=self)]
        if name:
            backends = [backend for backend in backends if backend.name()==name]
        return backends
    
    def __str__(self):
        return 'JuqcsProvider'
