from loudspeakers.Unit import *


class Parameter(object):
    def __init__(self, name, description="", unit=NoUnit):
        self.name = name
        self.description = description
        self.unit = unit
        self.value = None
        self.is_provided = False

    def set(self, other):
        if self.unit.is_consistent(other.unit):
            self.set_value(other.value * other.unit.factor / self.unit.factor, self.unit)
        else:
            print("Unit mismatch!")

    def set_value(self, value, unit=NoUnit):
        if value is not None:
            self.is_provided = True
        if unit is not None:
            if self.unit.is_consistent(unit):
                self.unit = unit
            else:
                print("Unit {} is not compatible with parameter {} (unit should be {} or a sub-unit of it)"
                      .format(unit.symbol, self.name, self.unit.symbol))
        self.value = value
        print("{} = {} {} [{}]".format(self.name, self.value, self.unit.name, self.unit.get_in_SI()))

    def __mul__(self, other):
        result = Parameter(name="{} x {}".format(self.name, other.name),
                           description="{} by {}".format(self.description, other.description),
                           unit=self.unit * other.unit)
        result.set_value(self.value * other.value, self.unit * other.unit)
        return result

    @property
    def get(self):
        return self.value * self.unit.factor
