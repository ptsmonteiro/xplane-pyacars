from flightPhase import FlightPhase
from dataref import DataRef
from logger import Logger
from aircraft import Aircraft

class Flight:
    '''
    Flight information
    '''

    def __init__(self):
        self.reset()

    def reset(self):
        # flight plan info
        self.online_pilot_id = ''
        self.number = ''
        self.origin = ''
        self.destination = ''
        self.alternate = ''
        self.route = ''
        self.altitude = ''
        self.speed = ''
        self.enroute_time = 0 # unix timestamp
        self.departure_time = 0 # unix timestamp
        self.aircraft_type = ''
        self.flight_type = 'V'
        self.registration = ''

        # times
        self.block_out_time = 0
        self.take_off_time = 0
        self.landing_time = 0
        self.block_in_time = 0

    def import_from_xsb(self):
        try:
            xsb_status = DataRef.get_i("xsquawkbox/login/status")
            if (xsb_status != 1):
                Logger.log("XSquawkbox not online. Skipping.")
                return
        except:
            Logger.log("XSquawkbox not found")
            return -1

        Logger.log("Importing flight plan from XSquawkbox")
        self.online_pilot_id = DataRef.get_string("xsquawkbox/login/pilot_id")
        self.number = DataRef.get_string('xsquawkbox/login/callsign')
        self.aircraft_type = DataRef.get_string("xsquawkbox/login/model")
        self.flight_type = DataRef.get_i("xsquawkbox/fp/flight_type")           # int, either I, V, D, or S
        self.origin = DataRef.get_string("xsquawkbox/fp/departure_airport")		# string, ICAO code
        self.altitude = DataRef.get_string("xsquawkbox/fp/cruise_altitude")	    # string, either FLxxx or yyyyy
        self.destination = DataRef.get_string("xsquawkbox/fp/arrival_airport")	# string, ICAO code
        self.alternate = DataRef.get_string("xsquawkbox/fp/alternate_airport")	# string, ICAO code
        self.route = DataRef.get_string("xsquawkbox/fp/route")					
        self.remarks = 'Imported from XSquawkbox'

    def set_origin_from_current_pos(self):
        airport = self.aircraft.find_nearest_airport()
        self.origin = airport['icao']

    def set_destination_from_current_pos(self):
        airport = self.aircraft.find_nearest_airport()
        self.destination = airport['icao']

    def set_destination_from_fms(self):
        airport = self.aircraft.find_fms_destination_airport()
        if airport is None:
            return
        self.destination = airport['icao']
