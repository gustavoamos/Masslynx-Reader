''' 
    Waters 
    MassLynx Python SDK
'''

from .MassLynxProcessorBase import MassLynxProcessorBase
from .MassLynxRawDefs import MassLynxBaseType

from .Providers.MassLynxRawScanProcessorProvider import MassLynxRawScanProcessorProvider

class MassLynxScanProcessor(MassLynxProcessorBase):
    """
	Provides processing for scans
	Initially scan must be loaded or combined to produce a scan for subsequent processing
    """
   
    def __init__(self ):
        super().__init__( MassLynxBaseType.SCAN, MassLynxRawScanProcessorProvider())

    def GetScan( self ):
        """
        Returns the processed scan

        @return array of masses, array of intensities

        """
        code, masses, intensities = self._provider.GetScan()
        super().CheckReturnCode( code )
        return masses, intensities

    def Load( self, whichFunction, whichScan ):
        """
        Loads single scan into the processor

        @param  whichFunction requested function
        @param  whichScan 

        """
        self.Combine(whichFunction, whichScan, whichScan)
        return self

    def LoadDrift( self, whichFunction, whichScan, whichDrift ):
        """
        Loads single drift scan into the processor

        @param  whichFunction requested function
        @param  whichScan
        @param  whichDrift

        """
        self.CombineDrift(whichScan, whichScan, whichDrift, whichDrift)
        return self

    def Combine( self, whichFunction, startScan, endScan ):
        """
        Combines range of scans

        @param  whichFunction requested function
        @param  startScan
        @param  endScan

        """
        code = self._provider.CombineScan(whichFunction, startScan, endScan )
        super().CheckReturnCode( code )
        return self

    def CombineDrift( self, whichFunction, startScan, endScan, startDrift, endDrift ):
        """
        Combines range of drift scans

        @param  whichFunction requested function
        @param  startScan
        @param  endScan
        @param  startDrift
        @param  endDrift

        """
        code = self._provider.CombineDriftScan(whichFunction, startScan, endScan, startDrift, endDrift )
        super().CheckReturnCode( code )
        return self
        
    def Centroid(self):
        """
        Centroids the spectrum in the processor using values set in the processor
        """
        code = self._provider.Centroid()
        super().CheckReturnCode( code )
        return self

    def GetCentroidParameters(self):
        """
        Returns the centroid parameters set in the processor

        @return CentroidParameter key / value pairs

        """
        code, parameters = self._provider.GetCentroidParameter()
        super().CheckReturnCode( code )
        return parameters

    def Smooth(self):
        """
        Smooths the spectrum in the processor using values set in the processor

        """
        code = self._provider.SmoothScan()
        super().CheckReturnCode( code )
        return self

    def SetSmoothParameters( self, parameters ):
        """
        Sets the smooth parameters
        Parameters are supplied in a key value pair in the MassLynxParameter class

        Key	Description
        SmoothParameter::NUMBER
        SmoothParameter::WIDTH
        SmoothParameter::TYPE	SmoothType::MEAN,  SmoothType::MEDIAN or SmoothType::SAVITZKY_GOLAY

        """
        code = self._provider.SetSmoothParameter(parameters)
        super().CheckReturnCode( code )
        return self

    def GetSmoothParameters(self):
        """
        Smooths the spectrum in the processor using the supplied values
        Parameters are supplied in a key value pair in the MassLynxParameter class

        @param  MassLynxParameters SmoothParameter key / value pairs

        """
        code, parameters = self._provider.GetSmoothParameter()
        super().CheckReturnCode( code )
        return parameters

    def Threshold(self):
        """
        Thresholds the spectrum in the processor using values set in the processor

        """
        code = self._provider.ThresholdScan()
        super().CheckReturnCode( code )
        return self

    def SetThresholdParameters( self, parameters ):
        """
        Sets the threshold parameters
        Parameters are supplied in a key value pair in the MassLynxParameter class

        Key	Description
        ThresholdParameter::VALUE			
        ThresholdParameter::TYPE	ThresholdType::ABSOLUTE_THRESHOLD or ThresholdType::RELATIVE_THRESHOLD 

        """
        code = self._provider.SetThresholdParameter(parameters)
        super().CheckReturnCode( code )
        return self
