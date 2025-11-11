''' 
    Waters 
    MassLynx Python SDK
'''

from ctypes import c_char_p, c_void_p
from .MassLynxParameters import MassLynxParameters
from .Providers.MassLynxProvider import MassLynxProvider

class MassLynxLicense(object):

    @staticmethod
    def CheckLicense(userLicense):
        """
        Returns information about the license and version of the MassLynx SDK.
        The user license key should match the MassLynx SDK version

        @param  licenseKey - the user license key

        @return MassLynxParameters - LicenseParameter key / value pairs
        """
        bytes = str.encode(userLicense)
        params = MassLynxParameters()
        getLicenseInfo = MassLynxProvider.MassLynxDll.getLicenseInfo
        getLicenseInfo.argtypes = [c_char_p , c_void_p]
        code = getLicenseInfo(bytes, params.GetParameters())
        return params