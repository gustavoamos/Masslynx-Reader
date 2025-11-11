'''
     Waters 
    MassLynx Python SDK
'''

from ctypes import*

from .MassLynxProvider import MassLynxProvider
from .MassLynxReaderBaseProvider import MassLynxReaderBaseProvider

class MassLynxRawScanReaderProvider(MassLynxReaderBaseProvider):
     
    def ReadScan(self, whichFunction, whichScan):
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()

        # read scan
        readScan = MassLynxProvider.MassLynxDll.readScan
        readScan.argtypes = [c_void_p, c_int, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code = readScan(self._getReader(),whichFunction, whichScan,pMasses,pIntensities,size)

        # fill the array
        pM = cast(pMasses,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]
        
        return code, masses, intensities

    def ReadScanFlags( self, whichFunction, whichScan ):               
        # create the retrun values
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()
        pFlags = c_void_p()

        # read scan
        readScanFlags = MassLynxProvider.MassLynxDll.readScanFlags
        readScanFlags.argtypes = [c_void_p, c_int, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code= readScanFlags(self._getReader(),whichFunction,whichScan,pMasses,pIntensities,pFlags,size)

        # fill the array
        pM = cast(pMasses,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]

        # check for flags
        flags = []
        if None != pFlags.value:
            pF = cast(pFlags,POINTER(c_byte))
            flags = pF[0:size.value]

        return code, masses, intensities, flags

    def ReadDriftScan( self, whichFunction, whichScan, whichDrift ):             
        # create the retrun values
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()

        # read scan
        readDriftScan = MassLynxProvider.MassLynxDll.readDriftScan
        readDriftScan.argtypes = [c_void_p, c_int, c_int, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code =  readDriftScan(self._getReader(),whichFunction, whichScan, whichDrift, pMasses,pIntensities,size)

        # fill the array
        pM = cast(pMasses,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]
   
        return code, masses, intensities

    def ReadProductScan(self, whichFunction, whichScan):
        # create the retrun values
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()
        pProductMasses = c_void_p()
        productSize = c_int(0)

        readProductScan = MassLynxProvider.MassLynxDll.readProductScan
        readProductScan.argtypes = [c_void_p, c_int, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int), POINTER(c_int)]
        code =  readProductScan(self._getReader(),whichFunction, whichScan, pMasses, pIntensities, pProductMasses, size, productSize)

        # fill the array
        pM = cast(pMasses,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))
        pPM = cast(pProductMasses,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]
        productMasses = pPM[0:productSize.value]

        return code, masses, intensities, productMasses

    def GetMassScale(self, whichFunction, whichScan):
        # create the retrun values
        size = c_int(0)
        offset = c_int(0)
        pMasses = c_void_p()
        mlMethod = MassLynxProvider.MassLynxDll.getDriftMassScale
        mlMethod.argtypes = [c_void_p, c_int, c_int, POINTER(c_void_p), POINTER(c_int), POINTER(c_int)]
        code =  mlMethod(self._getReader(),whichFunction, whichScan, pMasses, size, offset)

        # fill the array
        pM = cast(pMasses,POINTER(c_float))

        masses = pM[0:size.value]

        return code, masses, offset.value
    
    def ReadDriftScanIndex(self, whichFunction, whichScan, whichDrift):
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()
        mlMethod =  MassLynxProvider.MassLynxDll.readDriftScanIndex
        mlMethod.argtypes = [c_void_p, c_int, c_int, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code =  mlMethod(self._getReader(), whichFunction, whichScan, whichDrift,  pMasses, pIntensities, size)

        # fill the array
        pM = cast(pMasses,POINTER(c_int))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]
    
        return code, masses, intensities
    
    def ReadDriftScanFlagsIndex(self, whichFunction, whichScan, whichDrift):
        size = c_int(0)
        pMasses = c_void_p()
        pIntensities = c_void_p()
        pFlags = c_void_p()

        mlMethod =  MassLynxProvider.MassLynxDll.readDriftScanFlagsIndex
        mlMethod.argtypes = [c_void_p, c_int, c_int, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code =  mlMethod(self._getReader(), whichFunction, whichScan, whichDrift,  pMasses, pIntensities, pFlags, size)

        # fill the array
        pM = cast(pMasses,POINTER(c_int))
        pI = cast(pIntensities,POINTER(c_float))

        masses = pM[0:size.value]
        intensities = pI[0:size.value]

        # check for flags
        flags = []
        if None != pFlags.value:
            pF = cast(pFlags,POINTER(c_byte))
            flags = pF[0:size.value]

        return code, masses, intensities, flags
        