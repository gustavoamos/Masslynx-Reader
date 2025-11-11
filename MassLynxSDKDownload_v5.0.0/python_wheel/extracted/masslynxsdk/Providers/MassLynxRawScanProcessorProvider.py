'''
     Waters 
    MassLynx Python SDK
'''

from ctypes import*

from ..MassLynxParameters import MassLynxParameters

from .MassLynxProvider import MassLynxProvider
from .MassLynxProcessorBaseProvider import MassLynxProcessorBaseProvider

class MassLynxRawScanProcessorProvider(MassLynxProcessorBaseProvider):
    
    def CombineScan(self, whichFunction, startScan, endScan):
        mlFunction = MassLynxProvider.MassLynxDll.combineScan
        mlFunction.argtypes = [c_void_p, c_int, c_int, c_int]
        return mlFunction(self._getProcessor(), whichFunction, startScan, endScan)

    def CombineDriftScan(self, whichFunction, startScan, endScan, startDrift, endDrift):
        mlFunction = MassLynxProvider.MassLynxDll.combineDriftScan
        mlFunction.argtypes = [c_void_p, c_int, c_int, c_int,c_int, c_int]
        return mlFunction(self._getProcessor(), whichFunction, startScan, endScan, startDrift, endDrift) 

    def GetScan(self):
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()

        # read scan
        mlFunction = MassLynxProvider.MassLynxDll.getScan
        mlFunction.argtypes = [c_void_p, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code = mlFunction(self._getProcessor(),pMasses,pIntensities,size)

        # fill the array
        pM = cast(pMasses,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]
        
        return code, masses, intensities

    def Centroid(self):
        mlFunction = MassLynxProvider.MassLynxDll.centroidScan
        mlFunction.argtypes = [c_void_p]
        return mlFunction(self._getProcessor()) 

    def GetCentroidParameter( self):     
        parameters = MassLynxParameters()
        mlFunction = MassLynxProvider.MassLynxDll.getCentroidParameter
        mlFunction.argtypes = [c_void_p, c_void_p]
        code = mlFunction(self._getProcessor(), parameters.GetParameters())
        return code, parameters

    def SmoothScan( self):     
        mlFunction = MassLynxProvider.MassLynxDll.smoothScan
        mlFunction.argtypes = [c_void_p]
        return mlFunction(self._getProcessor()) 

    def SetSmoothParameter(self, parameters):
        mlFunction = MassLynxProvider.MassLynxDll.setSmoothParameter
        mlFunction.argtypes = [c_void_p, c_void_p]
        return mlFunction(self._getProcessor(), parameters.GetParameters())

    def GetSmoothParameter( self):     
        parameters = MassLynxParameters()
        mlFunction = MassLynxProvider.MassLynxDll.getSmoothParameter
        mlFunction.argtypes = [c_void_p, c_void_p]
        code = mlFunction(self._getProcessor(), parameters.GetParameters())
        return code, parameters

    def ThresholdScan(self):
        mlFunction = MassLynxProvider.MassLynxDll.thresholdScan
        mlFunction.argtypes = [c_void_p]
        return mlFunction(self._getProcessor())

    def SetThresholdParameter(self, parameters):
        mlFunction = MassLynxProvider.MassLynxDll.setThresholdParameter
        mlFunction.argtypes = [c_void_p, c_void_p]
        return mlFunction(self._getProcessor(), parameters.GetParameters())
