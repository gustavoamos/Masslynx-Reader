'''
     Waters 
    MassLynx Python SDK
'''

from .MassLynxRawReader import MassLynxRawReader
from .MassLynxRawDefs import MassLynxBaseType
from .Providers.MassLynxRawAnalogReaderProvider import MassLynxRawAnalogReaderProvider

class MassLynxRawAnalogReader(MassLynxRawReader):
    """
    Allows access to raw analog data and chanel information
    If an error is encountered then an exception will be throw, see exception codes and messages
    """
    def __init__(self, source, userlicense = "" ):
        super().__init__(source, MassLynxBaseType.ANALOG, MassLynxRawAnalogReaderProvider(), userlicense)
        
    def GetChannelCount( self ):
        """
        Returns the number of channels
        @return int number of channels
        """
        code, size = self._provider.GetChannelCount()
        super().CheckReturnCode( code )
        return size

    def ReadChannel( self, whichChannel ):
        """
        Reads the times and intensities for the requested channel

        @param  whichChannel requested channel

        @return array of times, array of intensities
        """
        code, times, intensities = self._provider.ReadChannel( whichChannel )
        super().CheckReturnCode( code )
        return times, intensities

    def GetChannelDescription( self, whichChannel ):
        """
        Returns the channel description

        @param  whichChannel requested channel

        @return string channel description
        """
        code, description = self._provider.GetChannelDescription( whichChannel )
        super().CheckReturnCode( code )
        return description

    def GetChannelUnits( self, whichChannel ):
        """
        Returns the channel units

        @param  whichChannel requested channel

        @return string channel units
        """
        code, units = self._provider.GetChannelUnits( whichChannel )
        super().CheckReturnCode( code )
        return units

   