'''
     Waters 
    MassLynx Python SDK
'''
from ctypes import*

from ..MassLynxRawReader import MassLynxStringHandler
from ..MassLynxParameters import MassLynxParameters

from .MassLynxProvider import MassLynxProvider
from .MassLynxReaderBaseProvider import MassLynxReaderBaseProvider

class MassLynxRawInfoReaderProvider(MassLynxReaderBaseProvider):

    def __init__( self ):
        self._stringHandler = MassLynxStringHandler()
        super().__init__()

    def ToString( self, pString, release = False ):
        return self._stringHandler.ToString( pString, release )
      
    def GetNumberofFunctions(self):
        size = c_int(0)
        getFunctionCount =  MassLynxProvider.MassLynxDll.getFunctionCount
        getFunctionCount.argtypes = [c_void_p, POINTER(c_int)]
        code = getFunctionCount(self._getReader(),size)
        return code, size.value

    def GetScansInFunction( self, whichFunction ):
        size = c_int(0)   
        getScanCount = MassLynxProvider.MassLynxDll.getScanCount
        getScanCount.argtypes = [c_void_p, c_int, POINTER(c_int)]
        code = getScanCount(self._getReader(),whichFunction,size)
        return code, size.value

    def GetAcquisitionMassRange( self, whichFunction ):
        lowMass = c_float(0)
        highMass = c_float(0)
        getAcquisitionMassRange = MassLynxProvider.MassLynxDll.getAcquisitionMassRange
        getAcquisitionMassRange.argtypes = [c_void_p, c_int, c_int, POINTER(c_float), POINTER(c_float)]
        code = getAcquisitionMassRange(self._getReader(),whichFunction, 0,lowMass,highMass)
        return code, lowMass.value, highMass.value

    def GetAcquisitionTimeRange( self, whichFunction ):
        startTime = c_float(0)
        endTime = c_float(0)
        getAcquisitionTimeRange = MassLynxProvider.MassLynxDll.getAcquisitionTimeRange
        getAcquisitionTimeRange.argtypes = [c_void_p, c_int, POINTER(c_float), POINTER(c_float)]
        code = getAcquisitionTimeRange(self._getReader(),whichFunction,startTime,endTime)
        return code, startTime.value, endTime.value

    def GetFunctionType( self, whichFunction ):
        functionType = c_int(0)
        getFunctionType = MassLynxProvider.MassLynxDll.getFunctionType
        getFunctionType.argtypes = [c_void_p, c_int, POINTER(c_int)]
        code = getFunctionType(self._getReader(),whichFunction, functionType)
        return code, functionType.value

    def GetFunctionTypeString( self, functionType ):
        temp = c_char_p()
        getFunctionTypeString = MassLynxProvider.MassLynxDll.getFunctionTypeString
        getFunctionTypeString.argtypes = [c_void_p, c_int, POINTER(c_char_p)]
        code =  getFunctionTypeString(self._getReader(),functionType, temp)
        return code, self.ToString( temp )

    def IsContinuum( self, whichFunction ):
        continuum = c_bool(0)
        isContinuum = MassLynxProvider.MassLynxDll.isContinuum
        isContinuum.argtypes = [c_void_p, c_int, POINTER(c_bool)]
        code =  isContinuum(self._getReader(),whichFunction, continuum)
        return code, continuum.value

    def GetIonMode( self, whichFunction ):
        ionMode = c_int()
        getIonMode = MassLynxProvider.MassLynxDll.getIonMode
        getIonMode.argtypes = [c_void_p, c_int, POINTER(c_int)]
        code = getIonMode(self._getReader(),whichFunction, ionMode )
        return code, ionMode.value

    def GetIonModeString( self, ionMode ):
        temp = c_char_p()
        getIonModeString = MassLynxProvider.MassLynxDll.getIonModeString
        getIonModeString.argtypes = [c_void_p, c_int, POINTER(c_char_p)]
        code = getIonModeString(self._getReader(),ionMode, temp )
        return code, self.ToString( temp )

    def GetHeaderItemValue( self, whichItems ):
        nItems = len(whichItems )
        items = (c_int * nItems)(*whichItems)
        params = MassLynxParameters()
        getHeaderItemValue = MassLynxProvider.MassLynxDll.getHeaderItemValue
        getHeaderItemValue.argtypes = [c_void_p, POINTER(c_int), c_int, c_void_p]
        code = getHeaderItemValue(self._getReader(), items, nItems, params.GetParameters())
        return code, params

    def GetScanItemValue( self, whichFunction, whichScan, whichItems ):
        nItems = len(whichItems )
        items = (c_int * nItems)(*whichItems)
        params = MassLynxParameters()
        getHeaderItemValue = MassLynxProvider.MassLynxDll.getScanItemValue
        getHeaderItemValue.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), c_int, c_void_p]
        code = getHeaderItemValue(self._getReader(), whichFunction, whichScan, items, nItems, params.GetParameters())
        return code, params

    def GetScanItemName( self, whichItems ):
        nItems = len(whichItems)
        items = (c_int * nItems)(*whichItems)
        params = MassLynxParameters()
        getScanItemName = MassLynxProvider.MassLynxDll.getScanItemName
        getScanItemName.argtypes = [c_void_p, POINTER(c_int), c_int, c_void_p]
        code = getScanItemName(self._getReader(), items, nItems, params.GetParameters())
        return code, params

    def GetAcquisitionInfo( self ):
        params = MassLynxParameters()
        mlMethod = MassLynxProvider.MassLynxDll.getAcquisitionInfo
        mlMethod.argtypes = [c_void_p, c_void_p]
        code = mlMethod(self._getReader(), params.GetParameters())
        return code, params

    def GetItemsInFunction( self, whichFunction ):
        params = MassLynxParameters()
        mlMethod = MassLynxProvider.MassLynxDll.getScanItemsInFunction
        mlMethod.argtypes = [c_void_p, c_int, c_void_p]
        code =  mlMethod(self._getReader(),whichFunction,params.GetParameters())
        return code, params

    def GetCollisionalCrossSection( self, driftTime, mass, charge ):
        ccs = c_float(0)
        mlMethod = MassLynxProvider.MassLynxDll.getCollisionalCrossSection
        mlMethod.argtypes = [c_void_p, c_float,c_float,c_int, POINTER(c_float)]
        code =  mlMethod(self._getReader(),driftTime,mass,charge,ccs)
        return code, ccs.value

    def GetDriftScanCount( self, whichFunction ):
        count = c_int(0)   
        mlMethod = MassLynxProvider.MassLynxDll.getDriftScanCount
        mlMethod.argtypes = [c_void_p, c_int, POINTER(c_int)]
        code = mlMethod(self._getReader(),whichFunction,count)
        return code, count.value

    def GetMRMCount( self, whichFunction ):
        count = c_int(0)   
        mlMethod = MassLynxProvider.MassLynxDll.getMRMCount
        mlMethod.argtypes = [c_void_p, c_int, POINTER(c_int)]
        code = mlMethod(self._getReader(),whichFunction,count)
        return code, count.value

    def GetRetentionTime( self, whichFunction, whichScan ):
        retentionTime = c_float(0)
        mlMethod = MassLynxProvider.MassLynxDll.getRetentionTime
        mlMethod.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]
        code = mlMethod(self._getReader(),whichFunction,whichScan,retentionTime)
        return code, retentionTime.value

    def GetDriftTime( self, whichDrift ):
        driftTime = c_float(0)
        mlMethod = MassLynxProvider.MassLynxDll.getDriftTime
        mlMethod.argtypes = [c_void_p, c_int, POINTER(c_float)]
        code = mlMethod(self._getReader(),whichDrift,driftTime)
        return code, driftTime.value

    def GetDriftTimeFromCCS( self, ccs, mass, charge ):
        driftTime = c_float(0)
        mlMethod = MassLynxProvider.MassLynxDll.getDriftTime_CCS
        mlMethod.argtypes = [c_void_p, c_float, c_float, c_int, POINTER(c_float)]
        code = mlMethod(self._getReader(),ccs, mass, charge, driftTime)
        return code, driftTime.value

    def CanLockMassCorrect( self ):
        canApply = c_bool(0)
        mlMethod =  MassLynxProvider.MassLynxDll.canLockMassCorrect
        mlMethod.argtypes = [c_void_p, POINTER(c_bool)]
        code = mlMethod(self._getReader(), canApply)
        return code, canApply.value

    def IsLockMassCorrected( self ):
        corrected = c_bool(0)
        mlMethod =  MassLynxProvider.MassLynxDll.isLockMassCorrected
        mlMethod.argtypes = [c_void_p, POINTER(c_bool)]
        code =  mlMethod(self._getReader(), corrected)
        return code, corrected.value

    def GetLockMassFunction( self ):
        hasLockMass = c_bool()
        whichFunction = c_int()
        mlMethod =  MassLynxProvider.MassLynxDll.getLockMassFunction
        mlMethod.argtypes = [c_void_p, POINTER(c_bool), POINTER(c_int)]
        code =  mlMethod(self._getReader(), hasLockMass, whichFunction)
        return code, hasLockMass.value, whichFunction.value

    def GetScanRangeFromTimeRange( self, whichFunction, startTime, endTime ):
        startScan = c_int()
        endScan = c_int()
        mlMethod =  MassLynxProvider.MassLynxDll.getScanRangeFromTimeRange
        mlMethod.argtypes = [c_void_p, c_int, c_float,c_float, POINTER(c_int), POINTER(c_int)]
        code =  mlMethod(self._getReader(), whichFunction, startTime, endTime, startScan, endScan)
        return code, startScan.value, endScan.value

    def GetDriftRangeFromTimeRange( self, whichFunction, startTime, endTime ):
        startDrift = c_int()
        endDrift = c_int()
        mlMethod =  MassLynxProvider.MassLynxDll.getDriftRangeFromTimeRange
        mlMethod.argtypes = [c_void_p, c_int, c_float,c_float, POINTER(c_int), POINTER(c_int)]
        code =  mlMethod(self._getReader(), whichFunction, startTime, endTime, startDrift, endDrift)
        return code, startDrift.value, endDrift.value
    
    def GetIndexRange( self, whichFunction, preCursorMass, preCursorTolerance ):
        startIndex = c_int()
        endIndex = c_int()
        mlMethod =  MassLynxProvider.MassLynxDll.getIndexRange
        mlMethod.argtypes = [c_void_p, c_int, c_float,c_float, POINTER(c_int), POINTER(c_int)]
        code =  mlMethod(self._getReader(), whichFunction, preCursorMass, preCursorTolerance * 2, startIndex, endIndex)
        return code, startIndex.value, endIndex.value

    def GetPrecursorMass( self, whichFunction, whichIndex ):
        mass = c_float()
        mlMethod =  MassLynxProvider.MassLynxDll.getPrecursorMass
        mlMethod.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]
        code =  mlMethod(self._getReader(), whichFunction, whichIndex, mass)
        return code, mass.value
    
    def GetIndexPrecursorMassRange( self, whichFunction, whichIndex ):
        startMass = c_float()
        endMass = c_float()
        mlMethod =  MassLynxProvider.MassLynxDll.getIndexPrecursorMassRange
        mlMethod.argtypes = [c_void_p, c_int, c_int, POINTER(c_float), POINTER(c_float)]
        code =  mlMethod(self._getReader(), whichFunction, whichIndex, startMass, endMass)
        return code, startMass.value, endMass.value

    def GetFunctionPrecursorMassRange( self, whichFunction ):
        startMass = c_float()
        endMass = c_float()
        mlMethod =  MassLynxProvider.MassLynxDll.getFunctionPrecursorMassRange
        mlMethod.argtypes = [c_void_p, c_int, POINTER(c_float), POINTER(c_float)]
        code =  mlMethod(self._getReader(), whichFunction, startMass, endMass)
        return code, startMass.value, endMass.value

