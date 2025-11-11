''' Waters 
    MassLynx Python Chromatogram reader SDK
'''

from .MassLynxRawReader import MassLynxRawReader
from .MassLynxRawDefs import MassLynxBaseType

from .Providers.MassLynxRawChromatogramProvider import MassLynxRawChromatogramProvider

class MassLynxRawChromatogramReader(MassLynxRawReader):
    """Read masslynx chromatogram data"""
    def __init__(self, source, userlicense = "" ):
        super().__init__(source, MassLynxBaseType.CHROM, MassLynxRawChromatogramProvider(), userlicense)
   
    def ReadTIC( self, whichFunction ):
        code, masses, intensities = self._provider.ReadTIC(whichFunction)
        super().CheckReturnCode( code )
        return masses, intensities

    def ReadBPI( self, whichFunction ):
        code, masses, intensities = self._provider.ReadBPI( whichFunction )
        super().CheckReturnCode( code )
        return masses, intensities

    def ReadMassChromatogram( self, whichFunction, whichMass, massWindow, products ):
        # just call multiple mass with list of 1
        whichMasses = [whichMass]
        code, times, intensities =  self._provider.ReadMassChromatograms( whichFunction, whichMasses, massWindow, products )
        super().CheckReturnCode( code )   
        return times, intensities[0]

    def ReadMassChromatograms( self, whichFunction, whichMasses, massWindow, products ):
        code, times, intensities =  self._provider.ReadMassChromatograms( whichFunction, whichMasses, massWindow, products )
        super().CheckReturnCode( code )
        return times, intensities

    def ReadMRMChromatogram( self, whichFunction, whichMRM ):
        # just call multiple MRM with list of 1
        whichMRMs = [whichMRM]
        code, times, intensities =  self._provider.ReadMRMChromatograms( whichFunction, whichMRMs )
        super().CheckReturnCode( code )
        return times, intensities[0]

    def ReadMRMChromatograms( self, whichFunction, whichMRMs ):
        code, times, intensities =  self._provider.ReadMRMChromatograms( whichFunction, whichMRMs )
        super().CheckReturnCode( code )
        return times, intensities

    def ReadSonarChromatogram( self, whichFunction, precursorMass, precursorMassWindow, mass, massWindow  ):
        code, times, intensities =  self._provider.ReadSonarChromatogram( whichFunction, precursorMass, precursorMassWindow,  mass, massWindow )
        super().CheckReturnCode( code )
        return times, intensities

    def ReadMobillogram( self, whichFunction, startScan, endScan, startMass, endMass  ):
        code, bins, intensities =  self._provider.ReadMobillogram( whichFunction, startScan, endScan, startMass, endMass )
        super().CheckReturnCode( code )
        return bins, intensities

## \cond   
class MassLynxRawChromatogramReaderEx(MassLynxRawChromatogramReader):
    def __init__(self, source, userlicense = "" ):
        super().__init__(source,userlicense)

    def ExtractByBins( self, whichFunction, startMass, endMass, startBlock, endBlock, startBin, endBin ):
        code, bins, intensities = self._provider.ExtractByBins(whichFunction, startMass, endMass, startBlock, endBlock,startBin, endBin )
        super().CheckReturnCode( code )
        return bins, intensities
## \endcond   