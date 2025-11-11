'''
     Waters 
    MassLynx Python SDK
'''

from .MassLynxRawReader import MassLynxRawReader
from. MassLynxRawDefs import MassLynxBaseType

from .Providers.MassLynxRawInfoReaderProvider import MassLynxRawInfoReaderProvider

class MassLynxRawInfoReader(MassLynxRawReader):

    def __init__(self, source, userlicense = "" ):
        super().__init__(source, MassLynxBaseType.INFO, MassLynxRawInfoReaderProvider(), userlicense)
        
    def GetNumberofFunctions( self ):
        code, size = self._provider.GetNumberofFunctions()
        super().CheckReturnCode( code )
        return size

    def GetScansInFunction( self, whichFunction ):
        code, size = self._provider.GetScansInFunction(whichFunction)
        super().CheckReturnCode( code )
        return size

    def GetAcquisitionMassRange( self, whichFunction ):
        code, lowMass, highMass = self._provider.GetAcquisitionMassRange( whichFunction )
        super().CheckReturnCode( code )
        return lowMass, highMass

    def GetAcquisitionTimeRange( self, whichFunction ):
        code, startTime, endTime = self._provider.GetAcquisitionTimeRange( whichFunction )
        super().CheckReturnCode( code )
        return startTime, endTime

    def GetFunctionType( self, whichFunction ):
        code, functionType = self._provider.GetFunctionType( whichFunction )
        super().CheckReturnCode( code )
        return functionType

    def GetFunctionTypeString( self, functionType ):
        code, functionTypeString = self._provider.GetFunctionTypeString( functionType )
        super().CheckReturnCode( code )
        return functionTypeString

    def IsContinuum( self, whichFunction ):
        code, continuum =  self._provider.IsContinuum( whichFunction )
        super().CheckReturnCode( code )
        return continuum

    def GetIonMode( self, whichFunction ):
        code, ionMode =  self._provider.GetIonMode( whichFunction )
        super().CheckReturnCode( code )
        return ionMode

    def GetIonModeString( self, ionMode ):
        code, ionModeString = self._provider.GetIonModeString( ionMode )
        super().CheckReturnCode( code )
        return ionModeString

    def GetRetentionTime( self, whichFunction, whichScan ):
        code, retentionTime = self._provider.GetRetentionTime( whichFunction, whichScan )
        super().CheckReturnCode( code )
        return retentionTime

    def GetDriftTime( self, whichDrift ):
        code, driftTime = self._provider.GetDriftTime( whichDrift )
        super().CheckReturnCode( code )
        return driftTime

    def GetDriftTimeFromCCS( self, ccs, mass, charge ):
        code, driftTime = self._provider.GetDriftTimeFromCCS( ccs, mass, charge )
        super().CheckReturnCode( code )
        return driftTime

    def GetCollisionalCrossSection( self, driftTime, mass, charge ):
        code, driftTime = self._provider.GetCollisionalCrossSection( driftTime, mass, charge )
        super().CheckReturnCode( code )
        return driftTime

    def GetDriftScanCount( self, whichFunction ):
        code, count = self._provider.GetDriftScanCount(whichFunction)
        super().CheckReturnCode( code )
        return count

    def GetMRMCount( self, whichFunction ):
        code, count = self._provider.GetMRMCount(whichFunction)
        super().CheckReturnCode( code )
        return count

    def IsLockMassCorrected( self ):
        code, corrected = self._provider.IsLockMassCorrected()
        super().CheckReturnCode( code )
        return corrected

    def CanLockMassCorrect( self ):
        code, canApply = self._provider.CanLockMassCorrect()
        super().CheckReturnCode( code )
        return canApply

    def GetLockMassFunction( self ):
        code, hasLockMass, whichFunction = self._provider.GetLockMassFunction()
        super().CheckReturnCode( code )
        return whichFunction

    def GetAcquisitionInfo( self ):
        code, params = self._provider.GetAcquisitionInfo()
        super().CheckReturnCode( code )
        return params

    def GetHeaderItemValue( self, whichItems ):
        code, params = self._provider.GetHeaderItemValue( whichItems )
        super().CheckReturnCode( code )
        return params

    def GetScanItemValue( self, whichFunction, whichScan, whichItems ):
        code, params = self._provider.GetScanItemValue( whichFunction, whichScan, whichItems )
        super().CheckReturnCode( code )
        return params

    def GetScanItemName(self, whichItems):
        code, params = self._provider.GetScanItemName( whichItems )
        super().CheckReturnCode( code )
        return params

    def GetItemsInFunction( self, whichFunction ):
        code, params = self._provider.GetItemsInFunction( whichFunction )
        super().CheckReturnCode( code )
        return params

    def GetScanRange( self, whichFunction, startTime, endTime ):
        code, startScan, endScan = self._provider.GetScanRangeFromTimeRange( whichFunction, startTime, endTime )
        super().CheckReturnCode( code )
        return startScan, endScan

    def GetDriftRange( self, whichFunction, startTime, endTime ):
        code, startDrift, endDrift = self._provider.GetDriftRangeFromTimeRange( whichFunction, startTime, endTime )
        super().CheckReturnCode( code )
        return startDrift, endDrift

## \cond   
class MassLynxRawInfoReaderEx(MassLynxRawInfoReader):
    def __init__(self, source, userlicense = "" ):
        super().__init__(source, userlicense)
    # sonar
    def GetSonarRange( self, whichFunction, preCursorMass, preCursorTolerance ):
        code, startIndex, endIndex = self._provider.GetIndexRange( whichFunction, preCursorMass, preCursorTolerance )
        super().CheckReturnCode( code )
        return startIndex, endIndex
    
    def GetPrecursorMass( self, whichFunction, whichIndex ):
        code, precursorMass = self._provider.GetPrecursorMass( whichFunction, whichIndex )
        super().CheckReturnCode( code )
        return precursorMass
    
    def GetIndexPrecursorMassRange( self, whichFunction, whichIndex ):
        code, startMass, endMass = self._provider.GetIndexPrecursorMassRange( whichFunction, whichIndex )
        super().CheckReturnCode( code )
        return startMass, endMass
    
    def GetFunctionPrecursorMassRange( self, whichFunction ):
        code, startMass, endMass = self._provider.GetFunctionPrecursorMassRange( whichFunction )
        super().CheckReturnCode( code )
        return startMass, endMass
## \endcond   