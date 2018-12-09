from loudspeakers.Unit import *

import numpy as np


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
        self.value = value * unit.factor
        # print("{} = {} {} [{}]".format(self.name, value, self.unit.name, self.unit.get_in_SI()))

    def __add__(self, other):
        if self.unit.is_consistent(other.unit):
            result = Parameter(name="{} + {}".format(self.name, other.name),
                               description=self.description,
                               unit=self.unit)
            result.set_value(self.value + other.value, self.unit)
            return result
        else:
            raise ValueError("{} [{}] and {} [{}] have incompatible units"
                             .format(self.name, self.unit.symbol, other.name, other.unit.symbol))

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, Parameter):
            new_unit = self.unit * other.unit
            result = Parameter(name="{} x {}".format(self.name, other.name),
                               description="{} by {}".format(self.description, other.description),
                               unit=new_unit)
            result.set_value(self.value * other.value, new_unit)
        else:
            result = Parameter(name="{} x {}".format(self.name, other),
                               description=self.description,
                               unit=self.unit)
            result.set_value(self.value * other, self.unit)
        return result

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Parameter):
            new_unit = self.unit / other.unit
            result = Parameter(name="({}) / ({})".format(self.name, other.name),
                               description="{} over {}".format(self.description, other.description),
                               unit=new_unit)
            result.set_value(self.value / other.value, new_unit)
        else:
            result = Parameter(name="({}) / ({})".format(self.name, other.name),
                               description=self.description,
                               unit=self.unit)
            result.set_value(self.value / other, self.unit)
        return result

    def __rtruediv__(self, other):
        if isinstance(other, Parameter):
            new_unit = other.unit / self.unit
            result = Parameter(name="{} / ({})".format(other.name, self.name),
                               description="{} over {}".format(other.description, self.description),
                               unit=new_unit)
            result.set_value(other.value / self.value, new_unit)
        else:
            new_unit = self.unit.to_power(-1)
            result = Parameter(name="{} / ({})".format(other, self.name),
                               description="{} reciprocal".format(self.description),
                               unit=new_unit)
            result.set_value(other / self.value, new_unit)
        return result

    @property
    def get(self):
        return self.value * self.unit.factor


def sqrt(parameter):
    new_unit = parameter.unit.to_power(1/2)
    result = Parameter(name="({})^1/2".format(parameter.name),
                       description="square root of {}".format(parameter.description),
                       unit=new_unit)
    result.set_value(np.sqrt(parameter.value), new_unit)
    return result


def power(parameter: Parameter, index):
    new_unit = parameter.unit.to_power(index)
    result = Parameter(name="({})^{}".format(parameter.name, index),
                       description="{} to the power of {}".format(parameter.description, index),
                       unit=new_unit)
    result.set_value(np.power(parameter.value, index), new_unit)
    return result

