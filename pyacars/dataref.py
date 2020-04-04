'''
Dataref handling
'''

from XPLMDataAccess import *
from XPLMUtilities  import *
from XPLMPlugin     import *
from XPLMDefs       import *

class DataRef():
    '''
    X-Plane Dataref handler
    '''

    TYPE_INT = 0
    TYPE_DOUBLE = 1
    TYPE_FLOAT = 2
    TYPE_BIN = 4
    TYPE_VINT = 5
    TYPE_VFLOAT = 6

    def __init__(self, dataref, type, size = 1):
        self.dataref = XPLMFindDataRef(dataref)
        self.type = type
        self.size = size

        if (type == self.TYPE_INT):
            self.getter = XPLMGetDatai
            self.setter = XPLMSetDatai
        elif (type == self.TYPE_DOUBLE):
            self.getter = XPLMGetDatad
            self.setter = XPLMSetDatad
        elif (type == self.TYPE_FLOAT):
            self.getter = XPLMGetDataf
            self.setter = XPLMSetDataf
        elif (type == self.TYPE_BIN):
            self.getter = XPLMGetDatab
            self.setter = XPLMSetDatab
        elif (type == self.TYPE_VINT):
            self.getter = XPLMGetDatavi
            self.setter = XPLMSetDatavi
        elif (type == self.TYPE_VFLOAT):
            self.getter = XPLMGetDatavf
            self.setter = XPLMSetDatavf

    def read(self):
        if self.type in [self.TYPE_VINT, self.TYPE_VFLOAT]:
            value = self.getter(self.dataref, 0, self.size - 1)
        else:
            value = self.getter(self.dataref, 0)
        return value

    def write(self, value):
        if self.type in [self.TYPE_VINT, self.TYPE_VFLOAT]:
            self.setter(self.dataref, value, 0, self.size - 1)
        else:
            self.setter(self.dataref, value)

    @classmethod
    def get_i(cls, name):
        return XPLMGetDatai(XPLMFindDataRef(name))

    @classmethod
    def set_i(cls, name, value):
        return XPLMSetDatai(XPLMFindDataRef(name), value)


    @classmethod
    def get_f(cls, name):
        return XPLMGetDataf(XPLMFindDataRef(name))

    @classmethod
    def set_f(cls, name, value):
        return XPLMSetDataf(XPLMFindDataRef(name), value)


    @classmethod
    def get_d(cls, name):
        return XPLMGetDatad(XPLMFindDataRef(name))

    @classmethod
    def set_d(cls, name, value):
        return XPLMSetDatad(XPLMFindDataRef(name), value)


    @classmethod
    def get_vb(cls, name, limit = 1000):
        value = []
        XPLMGetDatab(XPLMFindDataRef(name), value, 0, limit)
        return value

    @classmethod
    def set_vb(cls, name, value):
        return XPLMSetDatab(XPLMFindDataRef(name), value, 0, len(value))


    @classmethod
    def get_vi(cls, name, limit = 1000):
        value = []
        XPLMGetDatavi(XPLMFindDataRef(name), value, 0, limit)
        return value

    @classmethod
    def set_vi(cls, name, value):
        return XPLMSetDatavi(XPLMFindDataRef(name), value, 0, len(value))


    @classmethod
    def get_vf(cls, name, limit = 1000):
        value = []
        XPLMGetDataf(XPLMFindDataRef(name), value, 0, limit)
        return value

    @classmethod
    def set_vf(cls, name, value):
        return XPLMSetDatavf(XPLMFindDataRef(name), value, 0, len(value))
