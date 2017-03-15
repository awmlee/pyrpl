from ..lockbox import *
from ..signals import *


class InterferometerPort1(InputDirect):
    def expected_signal(self, phase):
        return 0.5 * (self.min + self.max) +\
               0.5 * (self.max - self.min) * np.sin(phase)


class InterferometerPort2(InterferometerPort1):
    def expected_signal(self, phase):
        return super(InterferometerPort2, self).expected_signal(-phase)


class Interferometer(Lockbox):
    _units = ['m', 'deg', 'rad']
    wavelength = FloatProperty(max=10000, min=0, default=1.064e-6)
    _setup_attributes = ['wavelength']
    _gui_attributes = ['wavelength']
    variable = 'phase'

    inputs = LockboxModuleDictProperty(port1=InterferometerPort1,
                                       port2=InterferometerPort2)

    # pdh = InputPdh
    #    port1 = InterferometerPort1 # any attribute of type InputSignal will be instantiated in the model
    #    port2 = InterferometerPort2
    """
    @property
    def phase(self):
        if not hasattr(self, '_phase'):
            self._phase = 0
        return self._phase

    @phase.setter
    def phase(self, val):
        self._phase = val
        return val
    """

class PdhInterferometerPort1(InputIq, InterferometerPort1):
    def expected_signal(self, phase):
        # proportional to the derivative of the signal
        # i.e. sin(phase)+const. -> cos(phase)
        return 0.5 * (self.max - self.min) * np.cos(phase)

class PdhInterferometerPort2(InputIq, InterferometerPort2):
    def expected_signal(self, phase):
        # proportional to the derivative of the signal
        # i.e. sin(phase) -> cos(phase) = sin(phase+pi/2)
        return -0.5 * (self.max - self.min) * np.cos(phase)


class PdhInterferometer(Interferometer):
    inputs = LockboxModuleDictProperty(port1=InterferometerPort1,
                                       pdh1=PdhInterferometerPort1)
