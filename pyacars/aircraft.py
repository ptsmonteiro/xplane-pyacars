from dataref import DataRef
from logger import Logger

from XPLMDataAccess import *
from XPLMUtilities  import *
from XPLMPlugin     import *
from XPLMDefs       import *
from XPLMNavigation import *

class Aircraft():

    def isenginerunning(self):
        n_engines = DataRef.get_i("sim/aircraft/engine/acf_num_engines")
        running = DataRef.get_vi("sim/flightmodel/engine/ENGN_running", n_engines)

        if 1 in running:
            return True

        return False

    def isonground(self):
        gear_force = DataRef.get_f("sim/flightmodel/forces/fnrml_gear")
        return gear_force > 0

    def groundspeed(self):
        return DataRef.get_f("sim/flightmodel/position/groundspeed")

    def isstopped(self):
        return self.groundspeed() < 1

    def height(self):
        return DataRef.get_i("sim/cockpit2/gauges/indicators/radio_altimeter_height_ft_pilot")

    def verticalspeed(self):
        return DataRef.get_i("sim/flightmodel/position/vh_ind_fpm")

    def find_nearest_airport(self):
        lat = DataRef.get_d('sim/flightmodel/position/latitude')
        lon = DataRef.get_d('sim/flightmodel/position/longitude')

        navref = XPLMFindNavAid(None, None, lat, lon, None, xplm_Nav_Airport)
        if (navref == XPLM_NAV_NOT_FOUND):
            return None

        outLat = []
        outLon = []
        outID = []
        outName = []
        XPLMGetNavAidInfo(navref, None, outLat, outLon, None, None, None, outID, outName, None)
        airport = {
            'icao': outID,
            'name': outName,
            'lat': outLat,
            'lon': outLon
        }
        Logger.info("Nearest airport is %s" % airport['icao'])
        return airport
    
    def find_fms_destination_airport(self):
        count = XPLMCountFMSEntries()

        outType = []
        outRef = []
        XPLMGetFMSEntryInfo(count - 1, outType, None, outRef, None, None, None)
        if outType != xplm_Nav_Airport:
            Logger.info('FMS destination is not an airport')
            return None

        outLat = []; outLon = []; outID = []; outName = []
        XPLMGetNavAidInfo(outRef, None, outLat, outLon, None, None, None, outID, outName, None)
        airport = {
            'icao': outID,
            'name': outName,
            'lat': outLat,
            'lon': outLon
        }
        Logger.info("FMS destination is %s" % airport['icao'])
        return airport
        
        