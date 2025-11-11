''' Waters 
    MassLynx Python SDK
'''

from ctypes import POINTER, c_char_p, c_int

from .MassLynxRawReader import MassLynxRawReader
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

    # three option true, false, throw exception
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
class MassLynxProcessorBase():
    
    def __init__(self, mlType, mlProvider):
        # provider - link to the dll
        self._provider = mlProvider
        self._codeHandler = MassLynxCodeHandler()

        self._codeHandler.CheckReturnCode( self._provider.createRawProcessor(mlType) )

    def SetRawData( self, source ):
        """
        Set the raw data to be processed

        @return void
        """
        if (isinstance(source, MassLynxRawReader)):
            self._codeHandler.CheckReturnCode(  self._provider.setRawReader( source ) )

        # did we fall through
        else:
            self._codeHandler.CheckReturnCode( 1 )
    
    def GetLastCode( self):
        """
        Returns the last code

        @return int
        """
        return self._codeHandler.GetLastCode()
    
    def GetLastMessage(self):
        """
        Returns the message associated with the last code

        @return string
        """
        return self._codeHandler.GetLastMessage()
    
    ## \cond
    def ToString( self, pString, release = False ):
        return self._stringHandler.ToString( pString, release )
    
    def CheckReturnCode(self, code, throw = True):
        return self._codeHandler.CheckReturnCode( code , throw )
    ## \endcond
