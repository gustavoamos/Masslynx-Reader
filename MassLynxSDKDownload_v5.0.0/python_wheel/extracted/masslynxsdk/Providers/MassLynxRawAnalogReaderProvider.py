'''
     Waters 
    MassLynx Python SDK
'''
from ctypes import*

from ..MassLynxRawReader import MassLynxStringHandler

from .MassLynxProvider import MassLynxProvider
from .MassLynxReaderBaseProvider import MassLynxReaderBaseProvider

class MassLynxRawAnalogReaderProvider(MassLynxReaderBaseProvider):

    def __init__( self ):
        self._stringHandler = MassLynxStringHandler()
        super().__init__()

    def ToString( self, pString, release = False ):
        return self._stringHandler.ToString( pString, release )
      
    def GetChannelCount(self):
        size = c_int(0)
        mlFunction =  MassLynxProvider.MassLynxDll.getChannelCount
        mlFunction.argtypes = [c_void_p, POINTER(c_int)]
        code = mlFunction(self._getReader(),size)
        return code, size.value

    def ReadChannel(self, whichChannel):
        size = c_int(0)
        pTimes = c_void_p()
        pIntensities = c_void_p()

        # read channel
        mlFunction = MassLynxProvider.MassLynxDll.readChannel
        mlFunction.argtypes = [c_void_p, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code = mlFunction(self._getReader(),whichChannel, pTimes ,pIntensities, size)

        # fill the array
        pT = cast(pTimes,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        times = pT[0:size.value]
        intensities = pI[0:size.value]
        
        return code, times, intensities

    def GetChannelDescription( self, whichChannel ):
        temp = c_char_p()
        mlFunction = MassLynxProvider.MassLynxDll.getChannelDesciption
        mlFunction.argtypes = [c_void_p, c_int, POINTER(c_char_p)]
        code =  mlFunction(self._getReader(),whichChannel, temp)
        return code, self.ToString( temp )

    def GetChannelUnits( self, whichChannel ):
        temp = c_char_p()
        mlFunction = MassLynxProvider.MassLynxDll.getChannelUnits
        mlFunction.argtypes = [c_void_p, c_int, POINTER(c_char_p)]
        code =  mlFunction(self._getReader(),whichChannel, temp)
        return code, self.ToString( temp )
