
from ctypes import POINTER, c_char_p, c_void_p
from .MassLynxProcessorBase import MassLynxCodeHandler, MassLynxStringHandler

from .Providers.MassLynxProvider import MassLynxProvider

class MassLynxSampleList(object):
    """
    Builds MassLynx sample list in tab delimited format
    The sample list can then be submitted using AutoLynx
    """

    def __init__(self):
        self._mlSampleList = c_void_p()              # instance variable
        self._codeHandler = MassLynxCodeHandler()
        self._stringHandler = MassLynxStringHandler()       
        createSampleList = MassLynxProvider.MassLynxDll.createSampleList
        createSampleList.argtypes = [POINTER(c_void_p)]
        self.CheckReturnCode(createSampleList(self._mlSampleList))

    # destroy the samplelist
    def __del__(self):
        destroySampleList = MassLynxProvider.MassLynxDll.destroySampleList
        destroySampleList.argtypes = [c_void_p]          
        destroySampleList( self._mlSampleList )

    # get the sample list in csv
    def ToString( self ):
        """
        Returns the sample list table in tab delimited format

        @return string
        """
        temp = c_char_p()
        sampleListToString = MassLynxProvider.MassLynxDll.sampleListToString
        sampleListToString.argtypes = [c_void_p, POINTER(c_char_p)]
        self.CheckReturnCode( sampleListToString(self._mlSampleList, temp) )
        return self._stringHandler.ToString( temp, False )

    def AddRow( self, row ):
        """
        Appends new row to the sample list <br>

        @param row key value pairs of MassLynxSampleList Items
        """
        addSampleListRow = MassLynxProvider.MassLynxDll.addSampleListRow
        addSampleListRow.argtypes = [c_void_p, c_void_p]
        return self.CheckReturnCode( addSampleListRow(self._mlSampleList, row.GetParameters()) )

    # get the error message
    def GetLastMessage(self):
        """
        Returns the last error code
        """
        return self._codeHandler.GetLastMessage()

    # get the error code
    def GetLastCode(self):
        """
        Returns the last error code
        """
        return self._codeHandler.GetLastCode()
    
    ## \cond
    # handle the retun code - no exceptions
    def CheckReturnCode( self, code ):
        return self._codeHandler.CheckReturnCode(code, False)
    ## \endcond
