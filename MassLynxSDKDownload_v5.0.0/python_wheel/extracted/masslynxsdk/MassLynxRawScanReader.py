''' Waters 
    MassLynx Python SDK
'''

from .MassLynxRawReader import MassLynxRawReader
from .MassLynxRawDefs import MassLynxBaseType

from .Providers.MassLynxRawScanReaderProvider import MassLynxRawScanReaderProvider

class MassLynxRawScanReader(MassLynxRawReader):
    """Read masslynx scan data"""
   
    def __init__(self, source, userlicense = "" ):
        super().__init__(source, MassLynxBaseType.SCAN, MassLynxRawScanReaderProvider(), userlicense)

    def ReadScan( self, whichFunction, whichScan ):
        """
        Reads the masses and intensities for the requested function and scan

        @param  whichFunction requested function
        @param  whichScan requested scan

        @return array of masses, array of intensities
        """
        code, masses, intensities = self._provider.ReadScan(whichFunction, whichScan)
        super().CheckReturnCode( code )
        return masses, intensities

    def ReadScanFlags( self, whichFunction, whichScan ):
        """
        Reads the masses, intensities and flags for the requested function and scan

        @param  whichFunction requested function
        @param  whichScan requested scan

        @return array of masses, array of intensities,  array of flags
        """
        code, masses, intensities, flags = self._provider.ReadScanFlags(whichFunction, whichScan)
        super().CheckReturnCode( code )
        return masses, intensities, flags

    def ReadDriftScan( self, whichFunction, whichScan, whichDrift ):
        """
        Reads the masses and intensities for the requested function, scan and drift

        @param  whichFunction requested function
        @param  whichScan requested scan
        @param  whichDrift requested drift

        @return array of masses, array of intensities
        """
        code, masses, intensities = self._provider.ReadDriftScan(whichFunction, whichScan, whichDrift)
        super().CheckReturnCode( code )
        return masses, intensities

    def ReadProductScan( self, whichFunction, whichScan ):   
        """
        Reads the masses, intensities and product masses for the requested function and scan

        @param  whichFunction requested function
        @param  whichScan requested scan

        @return array of masses, array of intensities, array of productMasses
        """
        code, masses, intensities, productMasses = self._provider.ReadProductScan(whichFunction, whichScan)
        super().CheckReturnCode( code )
        return masses, intensities, productMasses

## \cond    
class MassLynxRawScanReaderEx(MassLynxRawScanReader):
    def __init__(self, source, userlicense = ""):
        super().__init__(source, userlicense)

    def GetMassScale( self, whichFunction, whichScan  ):
        code, masses, startIndex = self._provider.GetMassScale(whichFunction, whichScan)
        super().CheckReturnCode( code )
        return masses, startIndex
    
    def ReadDriftScanIndex( self, whichFunction, whichScan, whichDrift  ):
        code, masses, intensities = self._provider.ReadDriftScanIndex(whichFunction, whichScan, whichDrift)
        super().CheckReturnCode( code )
        return masses, intensities

    def ReadDriftScanFlagsIndex( self, whichFunction, whichScan, whichDrift  ):
        code, masses, intensities, flags = self._provider.ReadDriftScanFlagsIndex(whichFunction, whichScan, whichDrift)
        super().CheckReturnCode( code )
        return masses, intensities, flags
## \endcond 