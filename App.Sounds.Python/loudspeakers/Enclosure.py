from loudspeakers.Parameter import Parameter
from loudspeakers.Unit import *


class Enclosure(object):
    def __init__(self, name, description="", enclosure_type=None):
        self.name = name
        self.description = description
        self.enclosure_type = enclosure_type
        self.bass_drivers = []
        self.internal_height = Parameter("Height", "Internal height of the enclosure", Meter)
        self.internal_width = Parameter("Width", "Internal width of the enclosure", Meter)
        self.internal_depth = Parameter("Depth", "Internal depth of the enclosure", Meter)
        self.internal_volume = Parameter("V", "Internal volume", Liter)

    def set_inner_dimensions(self, height, width, depth):
        self.internal_height.set_value(height, Meter)
        self.internal_width.set_value(width, Meter)
        self.internal_depth.set_value(depth, Meter)
        self.calculate_internal_volume()
        print("Internal volume [{}m x {}m x {}m]: {} {}".format(
            self.internal_height.value,
            self.internal_width.value,
            self.internal_depth.value,
            self.internal_volume.value,
            self.internal_volume.unit.symbol))

    def add_bass_driver(self, bass_driver):
        self.bass_drivers.append(bass_driver)

    def calculate_internal_volume(self):
        # self.internal_volume.set(
        #     1000.0 * self.internal_height.value * self.internal_width.value * self.internal_depth.value, Liter)
        self.internal_volume.set(self.internal_height * self.internal_width * self.internal_depth)
