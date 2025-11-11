'''
     Waters 
    MassLynx Python SDK
'''

from ctypes import*

from .MassLynxProvider import MassLynxProvider

class MassLynxProcessorBaseProvider(object):

    def __init__(self):
        self._mlProcessor = c_void_p()

    # destroy the processor
    def __del__(self):
        # destroy processor
        code = self.destroyRawProcessor()

    def _getProcessor(self):
        return self._mlProcessor

    def createRawProcessor(self, mlType):
        createRawProcessor = MassLynxProvider.MassLynxDll.createRawProcessor
        createRawProcessor.argtypes = [POINTER(c_void_p), c_int, c_void_p, POINTER(c_void_p)]
        return createRawProcessor(self._getProcessor(), mlType, c_void_p(0), c_void_p(0) )

    def destroyRawProcessor(self):
        destroyRawProcessor = MassLynxProvider.MassLynxDll.destroyRawProcessor
        destroyRawProcessor.argtypes = [c_void_p]
        destroyRawProcessor(self._getProcessor())

    def setRawPath( self, path ):
        bytes = str.encode(path)
        setRawPath = MassLynxProvider.MassLynxDll.setRawPath
        setRawPath.argtypes = [c_void_p, c_char_p]
        return setRawPath(self._getProcessor(), bytes)

    def setRawReader( self, mlReader ):
        setRawReader = MassLynxProvider.MassLynxDll.setRawReader
        setRawReader.argtypes = [c_void_p, c_void_p]
        return setRawReader(self._getProcessor(), mlReader._provider._getReader() )

  