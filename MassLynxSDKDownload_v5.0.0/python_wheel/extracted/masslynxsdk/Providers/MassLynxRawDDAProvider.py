'''
     Waters 
    MassLynx Python SDK
'''

from ctypes import*

from ..MassLynxParameters import MassLynxParameters

from .MassLynxProvider import MassLynxProvider
from .MassLynxProcessorBaseProvider import MassLynxProcessorBaseProvider

class MassLynxRawDDAProvider(MassLynxProcessorBaseProvider):
    def DDAGetScan(self, whichScan):
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()
        params = MassLynxParameters()

        # getnextscan
        mlMethod = MassLynxProvider.MassLynxDll.ddaGetScan
        mlMethod.argtypes = [c_void_p, c_int,  POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int), c_void_p]
        code = mlMethod(self._getProcessor(), whichScan, pMasses ,pIntensities ,size, params.GetParameters() )

        # fill the array
        pM = cast(pMasses,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]
        
        return code, masses, intensities, params

    def DDAGetNextScan(self): 
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()
        params = MassLynxParameters()
        pNext = c_bool(0)

        # getnextscan
        mlMethod = MassLynxProvider.MassLynxDll.ddaGetNextScan
        mlMethod.argtypes = [c_void_p, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int), c_void_p, POINTER(c_bool)]
        code = mlMethod(self._getProcessor(), pMasses ,pIntensities ,size, params.GetParameters(), pNext )

        # fill the array
        pM = cast(pMasses,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]
        
        return code, masses, intensities, params, pNext.value
    
    def DDAResetScan(self):
        # reset
        mlMethod = MassLynxProvider.MassLynxDll.ddaResetScan
        mlMethod.argtypes = [c_void_p]
        return mlMethod(self._getProcessor() )


    def DDAGetScanCount(self):
        count = c_int(0)

        # count
        mlMethod = MassLynxProvider.MassLynxDll.ddaGetScanCount
        mlMethod.argtypes = [c_void_p, POINTER(c_int)]
        code = mlMethod(self._getProcessor(), count )

        return code, count.value
    
    def SetDDAParameters(self, parameters):
        mlMethod = MassLynxProvider.MassLynxDll.setDDAParameters
        mlMethod.argtypes = [c_void_p, c_void_p]
        return mlMethod(self._getProcessor(), parameters.GetParameters())
    
    def DDAGetScanInfo(self, whichScan):
        params = MassLynxParameters()
        mlMethod = MassLynxProvider.MassLynxDll.ddaGetScanInfo
        mlMethod.argtypes = [c_void_p, c_int, c_void_p]
        code = mlMethod(self._getProcessor(), whichScan, params.GetParameters())
        return code, params

    def DDASetQuadIsolationWindow( self, parameters  ):
        mlMethod = MassLynxProvider.MassLynxDll.setQuadIsolationWindowParameters
        mlMethod.argtypes = [c_void_p, c_void_p]
        return mlMethod(self._getProcessor(), parameters.GetParameters())    
    
    def DDAGetQuadIsolationWindow( self ):
        params = MassLynxParameters()
        mlMethod = MassLynxProvider.MassLynxDll.getQuadIsolationWindowParameters
        mlMethod.argtypes = [c_void_p, c_void_p]
        code = mlMethod(self._getProcessor(), params.GetParameters())
        return code, params
