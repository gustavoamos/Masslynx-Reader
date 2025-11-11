''' 
    Waters 
    MassLynx Python SDK
'''

from .MassLynxProcessorBase import MassLynxProcessorBase
from .MassLynxRawDefs import MassLynxBaseType

from .Providers.MassLynxRawLockMassProvider import MassLynxRawLockMassProvider

class MassLynxLockMassProcessor(MassLynxProcessorBase):

    """
    Applies post acquisition lock mass correction to MassLynx data

    Lock mass correction can only be applied under certain conditions, data that has been lock mass corrected during acqusition can not be changed. To prevent unnecessary recalculation, comparison between the supplied parameters and the existing lock mass values is made. If these values are different then lock mass correction will be applied. If the 'force' parameter is set to true then lock mass correction will always be applied.

    If the lock mass algorithm has changed this will also force a recalculation of the lock mass correction.

    If an error is encountered then an exception will be throw, see exception codes and messages.
    """
    def __init__(self ):
        super().__init__( MassLynxBaseType.LOCKMASS, MassLynxRawLockMassProvider())

    def SetParameters( self, parameters ):
        """
        Sets the parameters into the lock mass processor. 
        Parameters are supplied in a key value pair in the MassLynxParameter class

        Key	Description
        LockMassParameter::MASS			Value of the lock mass
        LockMassParameter::TOLERANCE	Tolerance applied to the given lock mass used to find lock mass in data
        LockMassParameter::FORCE		Boolean value used to force the lock mass

        @param  lockMassParameters 
        """
        code = self._provider.SetLockMassParameters(parameters)
        super().CheckReturnCode( code )

    def GetParameters( self ):
        """
        Gets the parameters set in the lock mass processor.

        @return MassLynxParameters - LockMassParameterclass key / value pairs
        """
        code, parameters = self._provider.GetLockMassParameters()
        super().CheckReturnCode( code )
        return parameters

    def LockMassCorrect( self ):
        """
        Performs lock mass correction with the supplied parameters

        @return bool true if sucessfully lock mass correction is successful
        """
        code, success = self._provider.LockMassCorrect()
        super().CheckReturnCode( code )
        return success

    def RemoveLockMassCorrection( self ):
        """
        Removes post acquisition lock mass correction.

        """
        code = self._provider.RemoveLockMassCorrection()
        super().CheckReturnCode( code )
 
    def IsLockMassCorrected( self ):
        """
        Determines if the raw data has post acquisition lock mass correction applied.

        @return false if post acqustion lock mass correction is not applied.
        """
        code, applied = self._provider.IsLockMassCorrected()
        super().CheckReturnCode( code )
        return applied

    def CanLockMassCorrect( self ):
        """
        Determines if post acquisition lock mass correction can be applied.

        @return false if the raw data can not be lock mass corrected.
        """
        code, canCorrect = self._provider.CanLockMassCorrect()
        super().CheckReturnCode( code )
        return canCorrect

    def GetLockMassValues( self ):
        """
        Returns the currenty applied lock mass parameters

        @return MassLynxParameters
        Key	Description
        LockMassParameter::MASS			Value of the applied lock mass
        LockMassParameter::TOLERANCE	Tolerance applied to the given lock mass used to find lock mass in data
        """
        code, parameters = self._provider.GetLockMassParams()
        super().CheckReturnCode( code )
        return parameters

    def GetCorrection( self, retentionTime ):
        """
        Returns the currenty applied lockmass correction gain for a requested retention time

        @param retentionTime

        @return gain lock mass gain
        """
        code, gain = self._provider.GetLockMassCorrection(retentionTime)
        super().CheckReturnCode( code )
        return gain

    def GetCandidates( self ):
        """
        Returns the combined and centrioded spectrum of all lock mass scans
        Can be used to identify the lock mass

        @return [out] array of masses, array of intensities
        """
        code, masses, intensities = self._provider.GetCandidates()
        super().CheckReturnCode( code )

        return masses, intensities

    def AutoLockMassCorrect( self, force ):
        """
        Attempts to automatically apply lock mass correcion using known lock mass compounds
        @param force the data to be lockmass corrected, will overwrite any previous lockmass correction

        @return bool true if lock mass correction is successful
        """
        code, applied = self._provider.AutoLockMassCorrect(force)
        super().CheckReturnCode( code )

        return applied
