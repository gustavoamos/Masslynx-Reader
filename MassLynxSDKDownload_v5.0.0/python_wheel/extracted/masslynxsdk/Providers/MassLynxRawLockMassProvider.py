'''
     Waters 
    MassLynx Python SDK
'''

from ctypes import*

from ..MassLynxRawReader import MassLynxRawReader
from ..MassLynxParameters import MassLynxParameters

from .MassLynxProvider import MassLynxProvider
from .MassLynxProcessorBaseProvider import MassLynxProcessorBaseProvider

class MassLynxRawLockMassProvider(MassLynxProcessorBaseProvider):
    
    def SetLockMassParameters(self, parameters):
        setLockMassParameters = MassLynxProvider.MassLynxDll.setLockMassParameters
        setLockMassParameters.argtypes = [c_void_p, c_void_p]
        return setLockMassParameters(self._getProcessor(), parameters.GetParameters())

    def GetLockMassParameters( self):     
        parameters = MassLynxParameters()
        getLockMassParameters = MassLynxProvider.MassLynxDll.getLockMassParameters
        getLockMassParameters.argtypes = [c_void_p, c_void_p]
        code = getLockMassParameters(self._getProcessor(), parameters.GetParameters())

        return code, parameters

    def CanLockMassCorrect( self ):
        canApply = c_int(0)
        canLockMassCorrect =  MassLynxProvider.MassLynxDll.LMP_canLockMassCorrect
        canLockMassCorrect.argtypes = [c_void_p, POINTER(c_int)]
        code = canLockMassCorrect(self._getProcessor(), canApply)

        return code, canApply.value == 1 

    def IsLockMassCorrected( self ):
        applied = c_int(0)
        isLockMassCorrected =  MassLynxProvider.MassLynxDll.LMP_isLockMassCorrected
        isLockMassCorrected.argtypes = [c_void_p, POINTER(c_int)]
        code =  isLockMassCorrected(self._getProcessor(), applied)

        return code, applied.value == 1

    def LockMassCorrect( self ):   
        success = c_bool(0)   
        lockMassCorrect =  MassLynxProvider.MassLynxDll.lockMassCorrect
        lockMassCorrect.argtypes = [c_void_p, POINTER(c_bool)]
        code = lockMassCorrect(self._getProcessor(), success )

        return code, success.value

    def RemoveLockMassCorrection( self ):
        removeLockMassCorrection =  MassLynxProvider.MassLynxDll.removeLockMassCorrection
        removeLockMassCorrection.argtypes = [c_void_p]
        return removeLockMassCorrection(self._getProcessor())

    def GetLockMassParams( self ):  
        parameters = MassLynxParameters()
        getLockMassValuesParams =  MassLynxProvider.MassLynxDll.getLockMassValuesParams
        getLockMassValuesParams.argtypes = [c_void_p, c_void_p]
        code =  getLockMassValuesParams(self._getProcessor(), parameters.GetParameters())

        return code, parameters

    def GetLockMassCorrection( self, retentionTime ):  
        gain = c_float(0)
        getLockMassCorrection = MassLynxProvider.MassLynxDll.getLockMassCorrection
        getLockMassCorrection.argtypes = [c_void_p, c_float, POINTER(c_float)]
        code = getLockMassCorrection(self._getProcessor(), retentionTime, gain)

        return code, gain.value

    def GetCandidates( self ):
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()
        
        getLockMassCandidates =  MassLynxProvider.MassLynxDll.getLockMassCandidates
        getLockMassCandidates.argtypes = [c_void_p, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code = getLockMassCandidates(self._getProcessor(), pMasses, pIntensities,size)

        # fill the array
        pM = cast(pMasses,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]
        
        # dealocate memory
        MassLynxRawReader.ReleaseMemory( pMasses)
        MassLynxRawReader.ReleaseMemory( pIntensities)

        return code, masses, intensities

    def AutoLockMassCorrect( self, force ):   
        applied = c_bool(0)   
        mlMethod =  MassLynxProvider.MassLynxDll.autoLockMassCorrect
        mlMethod.argtypes = [c_void_p, c_bool, POINTER(c_bool)]
        code = mlMethod(self._getProcessor(), force, applied )

        return code, applied.value
