'''
pyACARS - X-plane ACARS plugin.
Copyright (C) 2020 Pedro Monteiro
---
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

# X-plane includes
from XPLMDefs import *
from XPLMProcessing import *
from XPLMDataAccess import *
from XPLMUtilities import *
from XPLMPlanes import *
from XPLMNavigation import *
from SandyBarbourUtilities import *
from PythonScriptMessaging import *
from XPLMPlugin import *
from XPLMMenus import *
from XPWidgetDefs import *
from XPWidgets import *
from XPStandardWidgets import *

import ctypes
import cPickle
import socket
import threading
import subprocess
import os
import signal
from datetime import datetime
from random import random

from pyacars import Conf
from pyacars import Recorder
from pyacars import DataRef
from pyacars import Logger

class PythonInterface:
    '''
    Xplane plugin
    '''
    def XPluginStart(self):
        self.syspath = []
        self.conf = Conf(XPLMGetSystemPath(self.syspath)[:-1])
        self.recorder = Recorder(self.conf)

        self.Name = "pyACARS - " + self.conf.__VERSION__
        self.Sig = "python.pyACARS"
        self.Desc = "ACARS, PIREP and Flight Data for Virtual Airlines"

        # floop
        self.floop = self.floopCallback
        XPLMRegisterFlightLoopCallback(self, self.floop, -1, 0)

        # Menu / About
        self.mPluginItem = XPLMAppendMenuItem(XPLMFindPluginsMenu(), 'pyACARS', 0, 1)
        self.mMain       = XPLMCreateMenu(self, 'pyACARS', XPLMFindPluginsMenu(), self.mPluginItem, self.mainMenuCB, 0)

        return self.Name, self.Sig, self.Desc

    def mainMenuCB(self, menuRef, menuItem):
        '''
        Main menu Callback
        '''
        Logger.log("mainMenuCB got menuRref: %d, menuItem: %d" % (menuRef, menuItem))

    def floopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        if DataRef.get_i("sim/time/paused"):
            return -1

        if DataRef.get_i('sim/operation/prefs/replay_mode'):
            return -1

        self.recorder.loop_callback()
        return -1

    def XPluginStop(self):
        XPLMUnregisterFlightLoopCallback(self, self.floop, 0)

        XPLMDestroyMenu(self, self.mMain)
        self.conf.pluginSave()

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        Logger.log("Received message %d from %d with param %d " % (inFromWho, inMessage, inParam))
