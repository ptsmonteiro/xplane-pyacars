import os
import cPickle
import sys
import subprocess

class Conf:
    '''
    Configuration variables
    '''
    syspath, dirsep = '', os.sep

    __VERSION__ = '0.0.1'

    def __init__(self, syspath):
        # Inits conf
        self.syspath      = syspath
        self.respath      = os.sep.join([self.syspath, 'Resources', 'plugins', 'PythonScripts', 'pyacars'])
        self.settingsfile = os.sep.join([self.respath, 'settings.pkl'])

        self.datapath    = os.sep.join([self.respath, 'data'])
        if not os.path.exists(self.datapath):
            os.makedirs(self.datapath)

        self.setDefautls()
        self.pluginLoad()

    def setDefautls(self):
        # Default and storable settings

        # Company Server
        self.company_flight_info_url    = 'https://zonexecutive.com/action.php/acars/xacars/data'
        self.company_pirep_url          = 'https://zonexecutive.com/action.php/acars/xacars/pirep'
        self.company_acars_url          = 'https://zonexecutive.com/action.php/acars/xacars/acars'
        self.company_fdr_url            = 'https://zonexecutive.com/action.php/acars/xacars/fdr'
        self.company_username           = 'ZE365'
        self.company_password           = 'yourpassword'

        # ACARS
        self.acars_report_interval_min = 1

    def saveSettings(self, filepath, settings):
        f = open(filepath, 'w')
        cPickle.dump(settings, f)
        f.close()

    def loadSettings(self, filepath):
        if os.path.exists(filepath):
            f = open(filepath, 'r')
            try:
                conf = cPickle.load(f)
                f.close()
            except:
                # Corrupted settings, remove file
                os.remove(filepath)
                return

            # may be "dangerous" if someone messes our config file
            for var in conf:
                if var in self.__dict__:
                    self.__dict__[var] = conf[var]

    def pluginSave(self):
        '''Save plugin settings'''
        conf = {
            'version' : self.__VERSION__,
            'company_flight_info_url' : self.company_flight_info_url,
            'company_pirep_url' : self.company_pirep_url,
            'company_acars_url' : self.company_acars_url,
            'company_fdr_url' : self.company_fdr_url,
            'company_username' : self.company_username,
            'company_password' : self.company_password,

            # ACARS
            'acars_report_interval_min' : self.acars_report_interval_min
        }
        self.saveSettings(self.settingsfile, conf)

    def pluginLoad(self):
        self.loadSettings(self.settingsfile)
