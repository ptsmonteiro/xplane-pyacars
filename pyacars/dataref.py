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

    @classmethod
    def get_xp_dataref(cls, name):
        ref = XPLMFindDataRef(name)
        if ref is None:
            raise Exception("Dataref not '%s' found" % name)
        else:
            return ref

    @classmethod
    def get_i(cls, name):
        return XPLMGetDatai(cls.get_xp_dataref(name))

    @classmethod
    def set_i(cls, name, value):
        return XPLMSetDatai(cls.get_xp_dataref(name), value)


    @classmethod
    def get_f(cls, name):
        return XPLMGetDataf(cls.get_xp_dataref(name))

    @classmethod
    def set_f(cls, name, value):
        return XPLMSetDataf(cls.get_xp_dataref(name), value)


    @classmethod
    def get_d(cls, name):
        return XPLMGetDatad(cls.get_xp_dataref(name))

    @classmethod
    def set_d(cls, name, value):
        return XPLMSetDatad(cls.get_xp_dataref(name), value)


    @classmethod
    def get_vb(cls, name, limit = 256):
        value = []
        XPLMGetDatab(cls.get_xp_dataref(name), value, 0, limit)
        return value

    @classmethod
    def get_string(cls, name, limit = 256):
        a = cls.get_vb(name, limit)
        return "".join(a)

    @classmethod
    def set_vb(cls, name, value):
        return XPLMSetDatab(cls.get_xp_dataref(name), value, 0, len(value))

    @classmethod
    def set_string(cls, name, value):
        cls.set_vb(name, map(ord, value))

    @classmethod
    def get_vi(cls, name, limit = 1000):
        value = []
        XPLMGetDatavi(cls.get_xp_dataref(name), value, 0, limit)
        return value

    @classmethod
    def set_vi(cls, name, value):
        return XPLMSetDatavi(cls.get_xp_dataref(name), value, 0, len(value))


    @classmethod
    def get_vf(cls, name, limit = 1000):
        value = []
        XPLMGetDataf(cls.get_xp_dataref(name), value, 0, limit)
        return value

    @classmethod
    def set_vf(cls, name, value):
        return XPLMSetDatavf(cls.get_xp_dataref(name), value, 0, len(value))
