from dataref import DataRef

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
