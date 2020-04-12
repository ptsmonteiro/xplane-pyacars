from logger import Logger

class FlightPhase:
    '''
    Flight Phase state machine
    '''

    PHASE_RAMP = 0
    PHASE_TAXI_OUT = 1
    PHASE_TAKEOFF = 2
    PHASE_CLIMB = 3
    PHASE_CRUISE = 4
    PHASE_DESCENT = 5
    PHASE_LANDING = 6
    PHASE_TAXI_IN = 7

    def __init__(self, aircraft):
        self.aircraft = aircraft
        self.reset()

    def reset(self):
        Logger.log('reseting flight phase')
        self.phase = self.PHASE_RAMP

    def update(self):
        oldphase = self.phase

        if self.phase == self.PHASE_RAMP:
            if self.aircraft.isenginerunning() and not self.aircraft.isstopped():
                self.phase = self.PHASE_TAXI_OUT

        elif self.phase == self.PHASE_TAXI_OUT:
            if self.aircraft.ias() > 35 and self.aircraft.height() < 500:
                self.phase = self.PHASE_TAKEOFF
            elif self.aircraft.isonground() and self.aircraft.isstopped() and not self.aircraft.isenginerunning():
                self.phase = self.PHASE_RAMP

        elif self.phase == self.PHASE_TAKEOFF:
            if (self.aircraft.verticalspeed() > 150 and self.aircraft.height() >= 500):
                self.phase = self.PHASE_CLIMB
            if (self.aircraft.verticalspeed() < -150 and self.aircraft.height() < 500):
                self.phase = self.PHASE_LANDING

        elif self.phase == self.PHASE_CLIMB:
            if abs(self.aircraft.verticalspeed()) < 150:
                self.phase = self.PHASE_CRUISE
            elif self.aircraft.verticalspeed() < -150:
                self.phase = self.PHASE_DESCENT

        elif self.phase == self.PHASE_CRUISE:
            if self.aircraft.verticalspeed() > 150:
                self.phase = self.PHASE_CLIMB
            elif self.aircraft.verticalspeed() < -150:
                self.phase = self.PHASE_DESCENT

        elif self.phase == self.PHASE_DESCENT:
            if self.aircraft.height() <= 500:
                self.phase = self.PHASE_LANDING

        elif self.phase == self.PHASE_LANDING:
            if self.aircraft.isonground() and self.aircraft.groundspeed() < 35:
                self.phase = self.PHASE_TAXI_IN
            elif self.aircraft.verticalspeed() > 150 and self.aircraft.height() >= 500:
                self.phase = self.PHASE_CLIMB

        elif self.phase == self.PHASE_TAXI_IN:
            if self.aircraft.isonground() and not self.aircraft.isenginerunning() and self.aircraft.isstopped():
                self.phase = self.PHASE_RAMP
            if self.aircraft.ias() > 35 and self.aircraft.height() < 500 and self.aircraft.verticalspeed() > 150:
                self.phase = self.PHASE_TAKEOFF

        if oldphase != self.phase:
            Logger.log("Phase change from %s to %s" % (oldphase, self.phase))

        return self.phase
