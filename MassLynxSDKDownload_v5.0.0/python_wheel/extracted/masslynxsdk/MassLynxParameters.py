from ctypes import POINTER, c_char_p, c_int, c_void_p, cast 

from .MassLynxRawReader import MassLynxStringHandler, MassLynxCodeHandler
from .Providers.MassLynxProvider import MassLynxProvider

class MassLynxParameters(object):
    """Create parameter"""

    def __init__(self):
        self._mlParameters = c_void_p()              # instance variable   
        self._codeHandler = MassLynxCodeHandler() 
        self._stringHandler = MassLynxStringHandler()
        createParameters = MassLynxProvider.MassLynxDll.createParameters
        createParameters.argtypes = [POINTER(c_void_p)]
        self.CheckReturnCode(createParameters(self._mlParameters))

    # destroy the samplelist
    def __del__(self):
        destroyParameters = MassLynxProvider.MassLynxDll.destroyParameters
        destroyParameters.argtypes = [c_void_p]          
        destroyParameters( self._mlParameters )

    # Set the key value pair
    def Set( self, key, value ):
        # is it a bool
        if isinstance(value, (bool)):
            if ( value ):
                value = 1
            else:
                value = 0

        # convert to string and encode
        bytes = str.encode(str(value))     
            
        setParameterValue = MassLynxProvider.MassLynxDll.setParameterValue
        setParameterValue.argtypes = [c_void_p, c_int, c_char_p]          
        setParameterValue( self._mlParameters, key, bytes )

        return self

    def Get( self, key ):
        # call the dll
        value = c_char_p()
        getParameterValue = MassLynxProvider.MassLynxDll.getParameterValue
        getParameterValue.argtypes = [c_void_p, c_int, POINTER(c_char_p)]
        getParameterValue(self._mlParameters, key, value )

        return self._stringHandler.ToString(value, False)

    def GetKeys( self):
        keys = []
           
        # create the retrun values
        size = c_int(0)
        pKeys = c_void_p()

        # get the keys
        getParameterKeys = MassLynxProvider.MassLynxDll.getParameterKeys
        getParameterKeys.argtypes = [c_void_p, POINTER(c_void_p), POINTER(c_int)]
        getParameterKeys(self._mlParameters,pKeys,size)

        # fill the array
        pK = cast(pKeys,POINTER(c_int))

        keys = pK[0:size.value]

        return keys
    
    ## \cond
    # get the parameter object
    def GetParameters(self):
        return self._mlParameters

    # handle the retun code - no exceptions
    def CheckReturnCode( self, code ):
        return self._codeHandler.CheckReturnCode(code, False)
    ## \endcond
