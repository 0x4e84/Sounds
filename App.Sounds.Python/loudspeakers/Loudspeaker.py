from loudspeakers.Parameter import Parameter
from loudspeakers.Unit import *


class Loudspeaker(object):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

        self.Re = Parameter("Re", "DC resistance of the voice coil", Ohm)
        self.Le = Parameter("Le", "Voice coil inductance", Henry)
        self.Fs = Parameter("Fs", "Resonance frequency of the driver", Hertz)

        # The quality factor describes the damping. A low Q value indicates an effective damping
        # Qms describes the damping of the suspension
        self.Qms = Parameter("Qms", "Mechanical quality factor", NoUnit)
        # Qes describes the damping caused by the coil-magnet assembly
        self.Qes = Parameter("Qes", "Electrical quality factor", NoUnit)
        # Total Q: 1/Qts = 1/Qms + 1/Qes
        self.Qts = Parameter("Qts", "Total quality factor", NoUnit)

        self.Sd = Parameter("Sd", "Projected area of the driver diaphragm", Meter2)
        self.Mms = Parameter("Mms", "Mass of the diaphragm/coil, including acoustic load", Kilogram)

        # Cms is the compliance of the suspension (the spider and the surround). A lower value indicates a stiff
        # suspension whereas a higher value indicates theat the suspension complies more easily
        self.Cms = Parameter("Cms", "Compliance of the driver's suspension", MetersPerNewton)
        self.Rms = Parameter("Rms", "Mechanical resistance of a driver's suspension", NewtonSecondPerMeter)

        # Vas describes the volume of the air inside a closed-box cabinet for which the compliance of the suspension
        # matches the compliance of the air inside the box.
        # If the enclosure volume is higher than Vas, we have an infinite baffle.
        # If the compliance of the suspension is at least 3 times the compliance of the air in the box,
        # we have an acoustic suspension enclosure.
        self.Vas = Parameter("Vas", "Equivalent volume of air", Meter3)
        self.Bl = Parameter("Bl", "Motor strength", TeslaMeter)

    def set_ts_parameters(self, re, le, fs, qms, qes, qts):
        print("Initializing Loudspeaker's Thiele and Small parameters:")
        self.Re.set_value(re, Ohm)
        self.Le.set_value(le, MilliHenry)
        self.Fs.set_value(fs, Hertz)
        self.Qms.set_value(qms)
        self.Qes.set_value(qes)
        self.Qts.set_value(qts)
        print("Calculated Qts = {}, provided value = {}".format(self.compute_qes(), self.Qts.value))

    def set_fundamental_parameters(self, sd, mms, cms, rms, bl, vas):
        print("Initializing Loudspeaker's fundamental parameters:")
        self.Sd.set_value(sd, Cm2)
        self.Mms.set_value(mms, Gram)
        self.Cms.set_value(cms, MillimeterPerNewton)
        self.Rms.set_value(rms, KiloPerSecond)
        self.Vas.set_value(vas, Liter)
        self.Bl.set_value(bl, TeslaMeter)

    def compute_qes(self):
        return (self.Qms.value * self.Qes.value) / (self.Qms.value + self.Qes.value)
