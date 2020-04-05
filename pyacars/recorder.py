import os
from aircraft import Aircraft
from flight import Flight
from flightPhase import FlightPhase
from dataref import DataRef
from datetime import datetime
from logger import Logger

class Recorder:
    '''
    Flight Data Recorder
    '''
    def __init__(self, conf):
        self.conf = conf
        self.aircraft = Aircraft()
        self.flight_phase = FlightPhase(self.aircraft)
        self.flight = Flight()
        self.time = 0
        self.sample_rate = 1 # Hz

        self.recording = False

        self.flush_interval_sec = 10
        self.flush_time = 0

        self.flight_data = []


    def loop_callback(self):
        time = DataRef.get_f('sim/time/total_flight_time_sec')

        # Sample rate limit
        if time - self.time < 1 / self.sample_rate:
            return
        
        self.update_status(time)
        self.time = time
        self.flight_phase.update()
        if not self.recording:
            Logger.log("Not recording")
            return

        self.record()

    def update_status(self, now):
        if self.recording:
            if now < self.time:
                Logger.log('flight was reset')
                self.flight_phase.reset()
                self.stop()
            if self.aircraft.isonground() and not self.aircraft.isenginerunning() and self.aircraft.isstopped():
                self.stop()
        elif self.aircraft.isonground() and self.aircraft.isenginerunning() and self.aircraft.isstopped() and now > 0:
                self.start()

        return self.recording

    def start(self):
        '''
        Start recording
        '''
        self.flight_data = []
        self.flush_time = 0
        filename = "recording-%s.csv" % datetime.now().strftime('%Y%m%d%H%M%S')
        filepath = os.sep.join([self.conf.datapath, filename])
        Logger.log("starting recording to file %s" % filepath)
        self.data_file = open(filepath, 'w')
        self.recording = True

    def stop(self):
        Logger.log('stopping recording')
        self.flush()
        self.data_file.close()
        self.recording = False

    def flush(self):
        '''
        Flush pending flight data to file
        '''
        Logger.log('flushing')

        if len(self.flight_data) < 1:
            return

        if self.flush_time == 0:
            # write headers
            headers = ';'.join(k for k in self.flight_data[0].keys())
            self.data_file.write("%s\n" % headers)

        for s in self.flight_data:
            line = ';'.join(str(s[k]) for k in s.keys())
            self.data_file.write("%s\n" % line)

        self.flush_time = self.time

    def record(self):
        Logger.log('recording sample')

        sample = {}

        # Recorded flight parameters
        sample['time_s'] = DataRef.get_f('sim/time/total_flight_time_sec')
        sample['altitude_ft'] = DataRef.get_f('sim/flightmodel/misc/h_ind')
        sample['latitude_deg'] = DataRef.get_f('sim/flightmodel/position/latitude')
        sample['longitude_deg'] = DataRef.get_f('sim/flightmodel/position/longitude')
        sample['gear_force'] = DataRef.get_f("sim/flightmodel/forces/fnrml_gear")
        sample['groundspeed_kt'] = DataRef.get_f("sim/flightmodel/position/groundspeed")
        sample['height_ft'] = DataRef.get_f("sim/cockpit2/gauges/indicators/radio_altimeter_height_ft_pilot")
        sample['ias_kt'] = DataRef.get_f("sim/flightmodel/position/indicated_airspeed")
        sample['vertical_speed_fpm'] = DataRef.get_f("sim/flightmodel/position/vh_ind_fpm")

        self.flight_data.append(sample)

        if self.time - self.flush_time >= self.flush_interval_sec:
            self.flush()
