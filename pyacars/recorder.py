import os
from aircraft import Aircraft
from flight import Flight
from flightPhase import FlightPhase
from dataref import DataRef
from datetime import datetime
from logger import Logger

class Recorder:

    METERS_PER_SEC_TO_KT = 1.943844
    METERS_PER_SEC_TO_FPM = 196.8504
    METERS_TO_FEET = 3.28084

    SAMPLE_RATE_HIGH_HZ = 10
    SAMPLE_RATE_MEDIUM_HZ = 1
    SAMPLE_RATE_LOW_HZ = 0.1

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

        # sample rate adjustment according to phase of flight
        if self.flight_phase.phase == self.flight_phase.PHASE_LANDING:
            self.sample_rate = self.SAMPLE_RATE_HIGH_HZ
        elif self.flight_phase.phase == self.flight_phase.PHASE_CRUISE:
            self.sample_rate = self.SAMPLE_RATE_LOW_HZ
        else:
            self.sample_rate = self.SAMPLE_RATE_MEDIUM_HZ

        if not self.recording:
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
        sample['time_s'] = round(DataRef.get_f('sim/time/total_flight_time_sec'),2)
        sample['baro_ref'] = round(DataRef.get_f('sim/cockpit/misc/barometer_setting'),2)

        sample['altitude_ft'] = round(DataRef.get_f('sim/flightmodel/misc/h_ind'))
        sample['vertical_speed_fpm'] = round(DataRef.get_f("sim/flightmodel/position/vh_ind_fpm"))
        sample['height_ft'] = round(DataRef.get_f("sim/cockpit2/gauges/indicators/radio_altimeter_height_ft_pilot"))
        sample['latitude_deg'] = DataRef.get_f('sim/flightmodel/position/latitude')
        sample['longitude_deg'] = DataRef.get_f('sim/flightmodel/position/longitude')
        sample['heading_deg'] = round(DataRef.get_f("sim/cockpit2/gauges/indicators/heading_vacuum_deg_mag_pilot"))
        sample['track_mag_deg'] = round(DataRef.get_f("sim/cockpit2/gauges/indicators/ground_track_mag_pilot"))

        sample['gear_force'] = round(DataRef.get_f("sim/flightmodel/forces/fnrml_gear"),1)

        sample['ias_kt'] = round(DataRef.get_f("sim/flightmodel/position/indicated_airspeed"))
        sample['tas_kt'] = round(DataRef.get_f("sim/cockpit2/gauges/indicators/true_airspeed_kts_pilot"))
        sample['mach_no'] = round(DataRef.get_f("sim/flightmodel/misc/machno"),2)
        sample['groundspeed_kt'] = round(DataRef.get_f("sim/flightmodel/position/groundspeed") * self.METERS_PER_SEC_TO_KT)

        sample['pitch_deg'] = round(DataRef.get_f("sim/flightmodel/position/true_theta"))
        sample['alpha_deg'] = round(DataRef.get_f("sim/flightmodel/position/alpha"))
        sample['load_factor_g'] = round(DataRef.get_f("sim/flightmodel/misc/g_total"),1)
        sample['bank_deg'] = round(DataRef.get_f("sim/flightmodel/position/true_phi"))
        sample['sideslip_deg'] = round(DataRef.get_f("sim/cockpit2/gauges/indicators/sideslip_degrees"))

        sample['cabin_alt_ft'] = round(DataRef.get_f("sim/cockpit/pressure/cabin_altitude_actual_m_msl") * self.METERS_TO_FEET)
        sample['cabin_vs_fpm'] = round(DataRef.get_f("sim/cockpit/pressure/cabin_vvi_actual_m_msec") * self.METERS_PER_SEC_TO_FPM)

        sample['nav1_freq_hz'] = round(DataRef.get_f("sim/cockpit/radios/nav1_freq_hz"),3)
        sample['nav1_nav_id'] = DataRef.get_string("sim/cockpit2/radios/indicators/nav1_nav_id")
        sample['nav1_hdev_dot'] = round(DataRef.get_f("sim/cockpit/radios/nav1_hdef_dot"),2)
        sample['nav1_vdef_dot'] = round(DataRef.get_f("sim/cockpit/radios/nav1_vdef_dot"),2)
        sample['dme_freq_hz'] = round(DataRef.get_f("sim/cockpit/radios/dme_freq_hz"),3)
        sample['dme_nav_id'] = DataRef.get_string("sim/cockpit2/radios/indicators/dme_nav_id")
        sample['dme_distance_nm'] = round(DataRef.get_f("sim/cockpit2/radios/indicators/hsi_dme_distance_nm_pilot"),1)

        sample['yoke_pitch'] = round(DataRef.get_f("sim/cockpit2/controls/yoke_pitch_ratio"),2)
        sample['yoke_roll'] = round(DataRef.get_f("sim/cockpit2/controls/yoke_roll_ratio"),2)
        sample['yoke_yaw'] = round(DataRef.get_f("sim/cockpit2/controls/yoke_heading_ratio"),2)

        sample['speedbrake_ratio'] = round(DataRef.get_f("sim/cockpit2/controls/speedbrake_ratio"),1)
        sample['flap_ratio'] = round(DataRef.get_f("sim/cockpit2/controls/flap_ratio"),1)
        sample['left_brake_ratio'] = round(DataRef.get_f("sim/cockpit2/controls/left_brake_ratio"),2)
        sample['right_brake_ratio'] = round(DataRef.get_f("sim/cockpit2/controls/right_brake_ratio"),2)
        sample['parking_brake_ratio'] = round(DataRef.get_f("sim/cockpit2/controls/parking_brake_ratio"),1)

        self.flight_data.append(sample)

        if self.time - self.flush_time >= self.flush_interval_sec:
            self.flush()
