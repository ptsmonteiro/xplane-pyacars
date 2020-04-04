from flightPhase import FlightPhase

class Flight:
    '''
    Flight information
    '''

    def __init__(self):
        self.reset()

    def reset(self):
        # flight plan info
        self.number = ''
        self.origin = ''
        self.destination = ''
        self.alternate = ''
        self.route = ''
        self.altitude = ''
        self.speed = ''
        self.enroute_time = 0 # unix timestamp
        self.departure_time = 0 # unix timestamp
        self.aircraft = ''
        self.registration = ''

        # times
        self.block_out_time = 0
        self.take_off_time = 0
        self.landing_time = 0
        self.block_in_time = 0
