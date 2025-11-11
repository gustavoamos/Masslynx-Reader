''' 
    Waters 
    MassLynx Python SDK
'''

from array import *
from .MassLynxProcessorBase import MassLynxProcessorBase
from .MassLynxRawDefs import DDAParameter, MassLynxBaseType
from .MassLynxParameters import MassLynxParameters

from .Providers.MassLynxRawDDAProvider import MassLynxRawDDAProvider

class MassLynxDDAProcessor(MassLynxProcessorBase):
    """
	Processes dda data returning MS1 and MS2 scans
	MS1 scan is the survey scan, MS2 is the associated fragment scan
    """

    def __init__(self ):
        super().__init__( MassLynxBaseType.DDA, MassLynxRawDDAProvider())

    def GetScanCount(self):
        """
        Returns the number of DDA scans
        Exception will be thrown on error

        @return number of scans
        """
        code, count = self._provider.DDAGetScanCount()
        super().CheckReturnCode( code )
        return count
    
    def SetCentroid(self, centroid ):
        """
        Set if spectra should be centroided as part of DDAProcessing.

        @param  bCentroid	True, spectra is centroided (default: False)
        """
        params = MassLynxParameters()
        params.Set( DDAParameter.CENTROID, centroid )
        code = self._provider.SetDDAParameters(params)
        super().CheckReturnCode( code )

    def GetScan(self, whichScan):
        """
        Get the scan at the index
        @param whichScan scan index

        @return array of masses, array of intensities, parameters MassLynxDDAIndexDetail key / value pairs
        """
        code, masses, intensities, params = self._provider.DDAGetScan(whichScan)
        return super().CheckReturnCode( code, False ), masses, intensities, params


    def GetNextScan(self):
        """
        Get the next available scan in the processor

        @return array of masses, array of intensities, parameters MassLynxDDAIndexDetail key / value pairs,  true if scan available
        """
        code, masses, intensities, params, bNext = self._provider.DDAGetNextScan()
        super().CheckReturnCode( code )
        return masses, intensities, params, bNext
    

    def GetScanInfo(self, whichScan):
        """
        Get information about the scan
        @param whichScan  scan index

        @return parameters MassLynxDDAIndexDetail key / value pairs
        """
        code, params = self._provider.DDAGetScanInfo(whichScan)
        return super().CheckReturnCode( code, False ), params
    
    def Reset(self):
        """
        Reset the next scan counter
        """
        code = self._provider.DDAResetScan()
        super().CheckReturnCode( code )

## \cond   
class MassLynxDDAProcessorEx(MassLynxDDAProcessor):
    def __init__(self  ):
        super().__init__()

    def SetQuadIsolationWindowParameters( self, parameters  ):
        code = self._provider.DDASetQuadIsolationWindow(parameters)
        super().CheckReturnCode( code )
    
    def GetQuadIsolationWindowParameters( self  ):
        code, parameters = self._provider.DDAGetQuadIsolationWindow()
        super().CheckReturnCode( code )
        return parameters
## \endcond   