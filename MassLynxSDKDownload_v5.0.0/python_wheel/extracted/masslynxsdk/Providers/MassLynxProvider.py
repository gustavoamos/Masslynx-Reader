'''
     Waters 
    MassLynx Python SDK
'''

import ctypes
import os
import sys

class MassLynxProvider(object):

    # load the dll
    MassLynxDll = None
    MassLynxPath = None

    dir = os.path.dirname(sys.modules['masslynxsdk'].__file__)

    if sys.platform.startswith('linux'):
        # load the shared library
        MassLynxPath = os.path.join(dir, 'Providers','lib','libMassLynxRaw.so')
        MassLynxDll = ctypes.CDLL(MassLynxPath)
    else:
        # load the dll
        MassLynxPath = os.path.join(dir, 'Providers','lib','MassLynxRaw.dll')
        MassLynxDll = ctypes.WinDLL(MassLynxPath)
