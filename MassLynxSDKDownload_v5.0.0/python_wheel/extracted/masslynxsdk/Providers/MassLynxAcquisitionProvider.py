from ctypes import*

from ..MassLynxParameters import MassLynxParameters
from .MassLynxProvider import MassLynxProvider

class MassLynxAcquisitionProvider(object):

    def __init__( self ):
        self._mlAcquisition = c_void_p()              # instance variable   

    # destroy the reader
    def __del__(self):
        # destroy acquisition
        self.destroyAcquisition()

    def createAcquisition(self):
        mlMethod = MassLynxProvider.MassLynxDll.createAcquisition
        mlMethod.argtypes = [POINTER(c_void_p)]
        return mlMethod(self._mlAcquisition)
    
    def destroyAcquisition(self):
        mlMethod = MassLynxProvider.MassLynxDll.destroyAcquisition
        mlMethod.argtypes = [c_void_p]
        mlMethod(self._mlAcquisition)

    def _getAcquisition(self):
        return self._mlAcquisition
    
    def getAutoLynxStatus(self):
        status = c_int(0) 
        mlMethod = MassLynxProvider.MassLynxDll.getAutoLynxStatus
        mlMethod.argtypes = [c_void_p, POINTER(c_int)]
        code = mlMethod(self._getAcquisition(), status )
        
        return code, status.value

    def getAutoLynxSettings(self):
        params = MassLynxParameters()

        # get the settings
        mlMethod = MassLynxProvider.MassLynxDll.getAutoLynxSettings
        mlMethod.argtypes = [c_void_p, c_void_p]
        code = mlMethod(self._getAcquisition(), params.GetParameters() )
        
        return code, params
    
    def getSampleListStatus(self, bytes):     
        status = c_int(0)
        mlMethod = MassLynxProvider.MassLynxDll.getSampleListStatus
        mlMethod.argtypes = [c_void_p, c_char_p, POINTER(c_int)]
        code = mlMethod(self._getAcquisition(), bytes, status)

        return code, status.value
    
    def abortAutoLynx(self, abort):     
        mlMethod = MassLynxProvider.MassLynxDll.abortAutoLynx
        mlMethod.argtypes = [c_void_p, c_bool]
        code = mlMethod(self._getAcquisition(), abort)

        return code
    
    def getStatus(self):
        status = MassLynxParameters()
        queue = MassLynxParameters()

        # get the settings
        mlMethod = MassLynxProvider.MassLynxDll.readStatus
        mlMethod.argtypes = [c_void_p, c_void_p,  c_void_p]
        code = mlMethod(self._getAcquisition(), status.GetParameters(), queue.GetParameters() )
        
        return code, status, queue
    
    def setStatusIniFile(self, bytes):     
        mlMethod = MassLynxProvider.MassLynxDll.setStatusIniFile
        mlMethod.argtypes = [c_void_p, c_char_p]
        code = mlMethod(self._getAcquisition(), bytes)

        return code
    
    def getStatusIniFile(self):
        params = MassLynxParameters()     
        mlMethod = MassLynxProvider.MassLynxDll.getStatusIniFile
        mlMethod.argtypes = [c_void_p, c_void_p]
        code = mlMethod(self._getAcquisition(), params.GetParameters())

        return code, params
    
    def getMassLynxInjection(self):
        params = MassLynxParameters()

        # get the settings
        mlMethod = MassLynxProvider.MassLynxDll.getMassLynxInjection
        mlMethod.argtypes = [c_void_p, c_void_p]
        code = mlMethod(self._getAcquisition(), params.GetParameters() )
        
        return code, params
    
    def setMassLynxInjectionFile(self, bytes):     
        mlMethod = MassLynxProvider.MassLynxDll.setMassLynxInjectionFile
        mlMethod.argtypes = [c_void_p, c_char_p]
        code = mlMethod(self._getAcquisition(), bytes)

        return code
    
    def getMassLynxInjectionFile(self):
        params = MassLynxParameters()     
        mlMethod = MassLynxProvider.MassLynxDll.getMassLynxInjectionFile
        mlMethod.argtypes = [c_void_p, c_void_p]
        code = mlMethod(self._getAcquisition(), params.GetParameters())

        return code, params
    
    def getMassLynxStatus(self):
        status = MassLynxParameters()
        queue = MassLynxParameters()

        # get the settings
        mlMethod = MassLynxProvider.MassLynxDll.getStatus
        mlMethod.argtypes = [c_void_p, c_void_p,  c_void_p]
        code = mlMethod(self._getAcquisition(), status.GetParameters(), queue.GetParameters() )
        
        return code, status, queue