'''
     Waters 
    MassLynx Python SDK
'''

from ctypes import*

from .MassLynxProvider import MassLynxProvider

class MassLynxReaderBaseProvider(object):

    def __init__( self ):
        self._mlRawReader = c_void_p()

    # destroy the reader
    def __del__(self):
        # destroy reader
        code = self.destroyRawReader()

    def _getReader(self):
        return self._mlRawReader
        
    def createRawReaderFromPath(self, bytes, mlType, license):
        mlMethod = MassLynxProvider.MassLynxDll.createRawReaderFromPath
        mlMethod.argtypes = [ c_char_p, POINTER(c_void_p), c_int, c_char_p]
        return mlMethod(bytes, self._getReader(), mlType, license)

    def createRawReaderFromReader(self, source, mlType):
        mlMethod = MassLynxProvider.MassLynxDll.createRawReaderFromReader
        mlMethod.argtypes = [ c_void_p, POINTER(c_void_p), c_int]
        return mlMethod(source._getReader(),self._getReader(),mlType)

    def destroyRawReader(self):
        mlMethod = MassLynxProvider.MassLynxDll.destroyRawReader
        mlMethod.argtypes = [c_void_p]          
        mlMethod( self._getReader() )

    def updateRawReader(self):
        mlMethod = MassLynxProvider.MassLynxDll.updateRawReader
        mlMethod.argtypes = [c_void_p]          
        return mlMethod( self._getReader() )

  