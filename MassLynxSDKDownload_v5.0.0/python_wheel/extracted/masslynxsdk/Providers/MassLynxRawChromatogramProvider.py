'''
     Waters 
    MassLynx Python SDK
'''

from ctypes import*

from ..MassLynxRawReader import MassLynxRawReader

from .MassLynxProvider import MassLynxProvider
from .MassLynxReaderBaseProvider import MassLynxReaderBaseProvider

class MassLynxRawChromatogramProvider(MassLynxReaderBaseProvider):
      
    def ReadTIC(self, whichFunction):
        times = []
        intensities = []

        # create the retrun values
        size = c_int(0)
        pTimes = c_void_p()
        pIntensities = c_void_p()
            
        # read tic
        readTIC = MassLynxProvider.MassLynxDll.readTICChromatogram
        readTIC.argtypes = [c_void_p, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code = readTIC(self._getReader(),whichFunction, pTimes, pIntensities, size)

        # fill the array
        pT = cast(pTimes,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        times = pT[0:size.value]
        intensities = pI[0:size.value]

        # dealocate memory
        MassLynxRawReader.ReleaseMemory( pTimes)
        MassLynxRawReader.ReleaseMemory( pIntensities)

        return code, times, intensities

    def ReadBPI( self, whichFunction ):
        # create the retrun values
        size = c_int(0)
        pTimes = c_void_p()
        pIntensities = c_void_p()
            
        # read tic
        readBPI = MassLynxProvider.MassLynxDll.readTICChromatogram
        readBPI.argtypes = [c_void_p, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code =  readBPI(self._getReader(),whichFunction, pTimes, pIntensities, size)

        # fill the array
        pT = cast(pTimes,POINTER(c_float))
        pI = cast(pIntensities,POINTER(c_float))

        times = pT[0:size.value]
        intensities = pI[0:size.value]

        # dealocate memory
        MassLynxRawReader.ReleaseMemory( pTimes)
        MassLynxRawReader.ReleaseMemory( pIntensities)

        return code, times, intensities

    def ReadMassChromatograms( self, whichFunction, whichMasses, massWindow, products ):
        times = []
        intensities = []

        # get the array of masses
        numMasses = len(whichMasses)
        masses = (c_float * numMasses)(*whichMasses)

        # create the retrun values
        size = c_int(0)
        pTimes = c_void_p()

        # create array of pointers to hold return intensities
        pIntensities = c_void_p()

        readMassChroms = MassLynxProvider.MassLynxDll.readMassChromatograms
        readMassChroms.argtypes = [c_void_p, c_int, POINTER(c_float), c_int, POINTER(c_void_p), POINTER(c_void_p), c_float, c_bool, POINTER(c_int)]
        code = readMassChroms( self._getReader(), whichFunction, masses, numMasses, pTimes, pIntensities, massWindow, products, size)

        # fill the array and free memory
        pT = cast(pTimes,POINTER(c_float))
        times = pT[0:size.value]
        MassLynxRawReader.ReleaseMemory( pTimes)

        # fill in the mass chroms and free memory
        pI = cast(pIntensities ,POINTER(c_float))
        for index in range(0, numMasses ):  
            intensities.append( pI[index * size.value :(index + 1)* size.value ])
        MassLynxRawReader.ReleaseMemory( pIntensities )

        return code, times, intensities

    def ReadMRMChromatograms( self, whichFunction, whichMRMs ):
        times = []
        intensities = []

        # get the array of masses
        numMRMs = len(whichMRMs)
        mrms = (c_int * numMRMs)(*whichMRMs)

        # create the retrun values
        size = c_int(0)
        pTimes = c_void_p()

        # create array of pointers to hold return intensities
        pIntensities = c_void_p()

        readMRMChroms = MassLynxProvider.MassLynxDll.readMRMChromatograms
        readMRMChroms.argtypes = [c_void_p, c_int, POINTER(c_int), c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code = readMRMChroms( self._getReader(), whichFunction, mrms, numMRMs, pTimes, pIntensities, size)

        # fill the array and free memory
        pT = cast(pTimes,POINTER(c_float))
        times = pT[0:size.value]
        MassLynxRawReader.ReleaseMemory( pTimes)

        # fill in the mass chroms and free memory
        pI = cast(pIntensities ,POINTER(c_float))
        for index in range(0, numMRMs ):  
            intensities.append( pI[index * size.value :(index + 1)* size.value ])
        MassLynxRawReader.ReleaseMemory( pIntensities )

        return code, times, intensities

    def ReadSonarChromatogram( self, whichFunction, precursorMass, precursorMassWindow,  mass, massWindow ):
        # create the retrun values
        size = c_int(0)
        pTimes = c_void_p()
        pIntensities = c_void_p()

        readSonarChroms = MassLynxProvider.MassLynxDll.readSonarMassChromatogram
        readSonarChroms.argtypes = [c_void_p, c_int,  c_float, c_float, POINTER(c_void_p), POINTER(c_void_p), c_float, c_float, POINTER(c_int)]
        code = readSonarChroms( self._getReader(), whichFunction, precursorMass, mass, pTimes, pIntensities, precursorMassWindow, massWindow, size)

        # fill the array and free memory
        pT = cast(pTimes,POINTER(c_float))
        times = pT[0:size.value]
        MassLynxRawReader.ReleaseMemory( pTimes)

        # fill in the mass chroms and free memory
        pI = cast(pIntensities ,POINTER(c_float))
        intensities = pI[0:size.value]
        MassLynxRawReader.ReleaseMemory( pIntensities )

        return code, times, intensities

    def ReadMobillogram( self, whichFunction, startScan, endScan, startMass, endMass ):
        # create the retrun values
        size = c_int(0)
        pBins = c_void_p()
        pIntensities = c_void_p()

        mlMethod = MassLynxProvider.MassLynxDll.readMobillogram
        mlMethod.argtypes = [c_void_p, c_int,  c_int, c_int, c_float, c_float, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code = mlMethod( self._getReader(), whichFunction, startScan, endScan, startMass, endMass, pBins, pIntensities, size)

        # fill the array and free memory
        pB = cast(pBins,POINTER(c_int))
        bins = pB[0:size.value]
        MassLynxRawReader.ReleaseMemory( pBins)

        # fill in the mass chroms and free memory
        pI = cast(pIntensities ,POINTER(c_float))
        intensities = pI[0:size.value]
        MassLynxRawReader.ReleaseMemory( pIntensities )

        return code, bins, intensities

    def ExtractByBins( self, whichFunction, massStart, massEnd, firstBlock, lastBlock, firstBin, lastBin ):
        # create the retrun values
        size = c_int(0)
        pBins = c_void_p()
        pIntensities = c_void_p()

        mlMethod = MassLynxProvider.MassLynxDll.extractByBins
        mlMethod.argtypes = [c_void_p, c_int, c_float, c_float, c_int, c_int, c_int, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]
        code = mlMethod( self._getReader(), whichFunction, massStart, massEnd, firstBlock, lastBlock, firstBin, lastBin, pBins, pIntensities, size)

        # fill the array and free memory
        pB = cast(pBins,POINTER(c_int))
        bins = pB[0:size.value]
        MassLynxRawReader.ReleaseMemory( pBins)

        # fill in the mass chroms and free memory
        pI = cast(pIntensities ,POINTER(c_float))
        intensities = pI[0:size.value]
        MassLynxRawReader.ReleaseMemory( pIntensities )

        return code, bins, intensities