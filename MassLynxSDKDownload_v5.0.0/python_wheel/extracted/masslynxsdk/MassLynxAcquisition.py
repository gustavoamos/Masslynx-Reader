
from .MassLynxRawDefs import AutoLynxStatus
from .MassLynxRawReader import MassLynxCodeHandler, MassLynxStringHandler 
from .Providers.MassLynxAcquisitionProvider import MassLynxAcquisitionProvider


class MassLynxAcquisition(object):
 
    """
	Allow sample submission using AutoLynx and access to current sample information
	
	Monitoring of the sample lists in the AutoLynx queue
	Paths to the status files will be initialised if running on a MassLynx system
	Optionally, the user can set the paths status files
	 
	Only available on Windows OS
	"""

    def __init__(self):
        self._codeHandler = MassLynxCodeHandler()
        self._stringHandler = MassLynxStringHandler()
        self._provider = MassLynxAcquisitionProvider()
        self._provider.createAcquisition()

    def __del__(self):
        # check the dtor
        self._provider = None

    def AutoLynxSettings(self):      
        """
        Returns the current AutoLynx settings

        @return MassLynxParameters - AutoLynxSettings key / value pairs
        @return MassLynxParameters
        """
        code, params = self._provider.getAutoLynxSettings()
        self.CheckReturnCode(code)
        return params

    def GetSampleListStatus(self, sampleListName):
        """
        Returns the status of the sample list in the AutoLynx queue

        @param name of the sample list. Note: Not the path
        @return AutoLynxStatus
        """
        bytes = str.encode(sampleListName)
        code, status = self._provider.getSampleListStatus(bytes)
        self.CheckReturnCode(code)
        return AutoLynxStatus(status)
    
    def GetAutoLynxStatus(self):
        """
        Returns the current AutoLynx status

        @return AutoLynxStatus
        """
        code, status = self._provider.getAutoLynxStatus()
        self.CheckReturnCode(code)
        return AutoLynxStatus(status)
    
    def AbortAutoLynx(self):
        """
        Sets the AutoLynx abort flag
        """
        code = self._provider.abortAutoLynx(True)
        self.CheckReturnCode(code)

    def ResumeAutoLynx(self):
        """
        Removes the AutoLynx abort flag 

        """
        code = self._provider.abortAutoLynx(False)
        self.CheckReturnCode(code)

    def SetStatusFile(self, fileName):
        """
        Set the path to the status ini file

        @param path to the status ini file  

        """
        bytes = str.encode(fileName)
        code = self._provider.setStatusIniFile(bytes)
        self.CheckReturnCode(code)

    def GetStatusFile(self):
        """
        Returns the path to the status ini file
        This can be used to monitor the file for updates

        @return string
        """
        code, params = self._provider.getStatusIniFile()
        self.CheckReturnCode(code)
        return params.Get(0)
    
    def GetMassLynxStatus(self):
        """
        Returns the current MassLynx status
        Exception will be thrown on error

        @return MassLynxParameters status containing key / value of MassLynxStatusType
        @return list containing the queue
        """
        code, status, queueParam = self._provider.getMassLynxStatus()
        self.CheckReturnCode(code)
        keys = queueParam.GetKeys()
        queue = []
        for i in keys:
            queue.append(queueParam.Get(i))

        return status, queue
    
    def TryGetMassLynxStatus(self):
        """
        Returns the current MassLynx status
        Exception will be thrown on error

        @return bool - True if successful
        @return MassLynxParameters status containing key / value of MassLynxStatusType
        @return list containing the queue
        """
        code, status, queueParam = self._provider.getMassLynxStatus()
        success = self.CheckReturnCode(code, False)
        keys = queueParam.GetKeys()
        queue = []
        for i in keys:
            queue.append(queueParam.Get(i))

        return success, status, queue
    
    def SetMassLynxInjectionFile(self, fileName):
        """
        Set the path to the MLCurSmp.txt file

        @param path to the  MLCurSmp.txt file

        """
        bytes = str.encode(fileName)
        code = self._provider.setMassLynxInjectionFile(bytes)
        self.CheckReturnCode(code)

    def GetMassLynxInjectionFile(self):
        """
        Returns the path to the MLCurSmp.txt file
        This can be used to monitor the file for updates

        @return string
        """
        code, params = self._provider.getMassLynxInjectionFile()
        self.CheckReturnCode(code)
        return params.Get(0)
    
    def GetMassLynxInjection(self):
        """
        Returns the current MassLynx injection
        Can be used to get the injection information when running processes from the MassLynx SampleList

        Exception will be thrown on error

        @return status containing key / value of MassLynxSampleListItem
        """
        code, params = self._provider.getMassLynxInjection()
        self.CheckReturnCode(code)
        return params
    
    def TryGetMassLynxInjection(self):
        """
        Returns the current MassLynx injection
        Can be used to get the injection information when running processes from the MassLynx SampleList

        Exception will be thrown on error

        @return bool, status containing key / value of MassLynxSampleListItem
        """
        code, params = self._provider.getMassLynxInjection()
        success = self.CheckReturnCode(code, False)
        return success, params
   
    def GetLastCode( self):     
        """
        Returns the last error code
        """
        return self._codeHandler.GetLastCode()
        
    def GetLastMessage(self):
        """
        Returns the last error code
        """
        return self._codeHandler.GetLastMessage()
    
    ##\cond
    def CheckReturnCode(self, code, throw = True):
        return self._codeHandler.CheckReturnCode( code , throw )
    ##\endcond