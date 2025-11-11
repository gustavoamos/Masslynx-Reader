''' Waters 
    MassLynx Python SDK
'''

from ctypes import POINTER, c_char_p, c_int, c_void_p

from .Providers.MassLynxProvider import MassLynxProvider

## \cond
class MassLynxException(Exception):
    code = 0
    def __init__(self, code, message):
        self.message = message
        self.code = code
    def __str__(self):
        return repr(  self.message )

    def Handler(self):
        #print( self.message )
        # can rethrow if needed
        return

# string handler
class MassLynxStringHandler(object):

    def __init__(self):
        return

    def ToString(self, chString, release):
        if (None == chString):
            return ""

        strValue  = chString.value.decode()
        if (release ):
            MassLynxRawReader.ReleaseMemory(chString)

        chString = None

        return strValue


class MassLynxCodeHandler(object):
    def __init__(self):
        self._code = 0
        self._stringHandler = MassLynxStringHandler()
        return

    # three options true, false, throw exception
    def CheckReturnCode( self, code, throw = True ):
        self._code = code
        if (0 == code):
            return True

        if (throw):
            raise MassLynxException( self.GetLastCode(), self.GetLastMessage() )

        # get last error
        return False

    def GetLastCode(self):
        return self._code

    def GetLastMessage(self):
        # load the dll
        getErrorMessage = MassLynxProvider.MassLynxDll.getErrorMessage
        getErrorMessage.argtypes = [ c_int, POINTER(c_char_p)]

        message = (c_char_p)()
        getErrorMessage( self.GetLastCode(), message )

        # release the memory
        return self._stringHandler.ToString(message, True)
## \endcond
    
class MassLynxRawReader():
    """basic functionality to read raw files"""
            
    def __init__(self, source, mlType, mlProvider, license):

        self._codeHandler = MassLynxCodeHandler()
        
        # provider - link to the dll
        self._provider = mlProvider

        # create scan reader from a path
        if (isinstance(source, str) ):
            bytes = str.encode(source)
            licensebytes = str.encode(license)
            code = self._provider.createRawReaderFromPath(bytes, mlType, licensebytes)
            self._codeHandler.CheckReturnCode(code)

        # create scan reader from a reader
        elif (isinstance(source, MassLynxRawReader)):
            # pass the provider
            code = self._provider.createRawReaderFromReader(source._provider, mlType)
            self._codeHandler.CheckReturnCode(code)
        
        # did we fall through
        else:
            self._codeHandler.CheckReturnCode( 1 )

    def Update( self ):
        code = self._provider.updateRawReader()
        self.CheckReturnCode(code)
    
    ## \cond
    def CheckReturnCode(self, code, throw = True):
        return self._codeHandler.CheckReturnCode( code , throw )

    # common util to free memory
    @staticmethod
    def ReleaseMemory( address):
        releaseMemory = MassLynxProvider.MassLynxDll.releaseMemory
        releaseMemory.argtypes = [ c_void_p]
        releaseMemory( address )
    ## \endcond