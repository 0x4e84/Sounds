class Unit(object):
    SI_units = ["m", "s", "kg", "mol", "Cd", "K", "A"]

    def __init__(self, meaning, name, symbol, factor=1.0, m=0, s=0, kg=0, mol=0, cd=0, k=0, a=0):
        self.SI_indexes = {}
        self.meaning = meaning
        self.name = name
        self.symbol = symbol
        self.factor = factor
        self.SI_indexes["m"] = m
        self.SI_indexes["s"] = s
        self.SI_indexes["kg"] = kg
        self.SI_indexes["mol"] = mol
        self.SI_indexes["Cd"] = cd
        self.SI_indexes["K"] = k
        self.SI_indexes["A"] = a
        print(name, self.get_in_SI())

    @classmethod
    def from_other_unit(cls, other, name=None, symbol=None, meaning=None, factor=1.0):
        return cls(meaning=other.meaning if meaning is None else meaning,
                   name=other.name if name is None else name,
                   symbol=other.symbol if symbol is None else symbol,
                   factor=factor,
                   m=other.SI_indexes["m"],
                   s=other.SI_indexes["s"],
                   kg=other.SI_indexes["kg"],
                   mol=other.SI_indexes["mol"],
                   cd=other.SI_indexes["Cd"],
                   k=other.SI_indexes["K"],
                   a=other.SI_indexes["A"])

    def __mul__(self, other):
        return Unit(meaning=self.meaning + " by " + other.meaning,
                    name=self.name + " * " + other.name,
                    symbol=self.symbol + "·" + other.symbol,
                    factor=self.factor * other.factor,
                    m=self.SI_indexes["m"] + other.SI_indexes["m"],
                    s=self.SI_indexes["s"] + other.SI_indexes["s"],
                    kg=self.SI_indexes["kg"] + other.SI_indexes["kg"],
                    mol=self.SI_indexes["mol"] + other.SI_indexes["mol"],
                    cd=self.SI_indexes["Cd"] + other.SI_indexes["Cd"],
                    k=self.SI_indexes["K"] + other.SI_indexes["K"],
                    a=self.SI_indexes["A"] + other.SI_indexes["A"])

    def __truediv__(self, other):
        return Unit(meaning=self.meaning + " over " + other.meaning,
                    name=self.name + " / " + other.name,
                    symbol=self.symbol + "/" + other.symbol,
                    factor=self.factor / other.factor,
                    m=self.SI_indexes["m"] - other.SI_indexes["m"],
                    s=self.SI_indexes["s"] - other.SI_indexes["s"],
                    kg=self.SI_indexes["kg"] - other.SI_indexes["kg"],
                    mol=self.SI_indexes["mol"] - other.SI_indexes["mol"],
                    cd=self.SI_indexes["Cd"] - other.SI_indexes["Cd"],
                    k=self.SI_indexes["K"] - other.SI_indexes["K"],
                    a=self.SI_indexes["A"] - other.SI_indexes["A"])

    def is_consistent(self, other):
        for key in self.SI_indexes:
            if self.SI_indexes[key] != other.SI_indexes[key]:
                return False
        return True

    def get_in_SI(self):
        numerator = []
        denominator = []
        for key, value in self.SI_indexes.items():
            if abs(value) == 1:
                s = key
            elif abs(value) == 2:
                s = key + "²"
            elif abs(value) == 3:
                s = key + "³"
            else:
                s = key + "^" + str(abs(value))

            if value < 0:
                denominator += [s]
            elif value > 0:
                numerator += [s]

        if not denominator:
            return "·".join(numerator)
        elif not numerator:
            return "1/" + "·".join(denominator)
        else:
            return "·".join(numerator) + "/" + "·".join(denominator)

# Fundamental SI units
# Meter — length.
# Distance traveled by light in a vacuum in 1/299,792,458 seconds.
Meter = Unit("Length", "Meter", "m", m=1)

# Second — time.
# Exactly 9,192,631,770 cycles of radiation of an atom of caesium-133.
Second = Unit("Time", "Second", "s", s=1)

# Kilogram — mass.
# Planck’s constant divided by 6.626,070,15 × 10−34 m−2s.
Kilogram = Unit("Mass", "Kilogram", "kg", kg=1)

# Mole — amount of substance.
# Avogadro constant, or 6.022,140,76 ×1023 elementary entities.
Mol = Unit("Amount of substance", "Mol", "mol", mol=1)

# Candela — luminous intensity.
# A light source with monochromatic radiation of frequency frequency 540 × 1012 Hz
# and radiant intensity of 1/683 watt per steradian.
Cd = Unit("Luminous intensity", "Candela", "Cd", cd=1)

# Kelvin — temperature.
# Boltzmann constant, or a change in thermal energy of 1.380 649 × 10−23 joules.
Kelvin = Unit("Temperature", "Kelvin", "K", k=1)

# Ampere — electric current.
# Equal to the flow of 1/1.602 176 634×10−19 elementary charges per second.
A = Unit("Electric current", "Ampere", "A", a=1)

# Derived units
Farad = Unit("Electrical Capacitance", "Farad", "F", kg=-1, m=-2, s=4, a=2)
Henry = Unit("Electrical Inductance", "Henry", "H", kg=1, m=2, s=-2, a=-2)
Hertz = Unit("Frequency", "Hertz", "Hz", s=-1)
Newton = Unit("Force", "Newton", "N", kg=1, m=1, s=-2)
Ohm = Unit("Electrical Impedance", "Ohm", "Ω", kg=1, m=2, s=-3, a=-2)
Tesla = Unit("Magnetic flux density", "Tesla", "T", kg=1, s=-2, a=-1)
Volt = Unit("Electric Potential", "Volt", "V", kg=1, m=2, s=-3, a=-1)

Meter2 = Unit.from_other_unit(Meter*Meter, "Surface", "Square Meters", "m²")
Meter3 = Unit.from_other_unit(Meter*Meter*Meter, "Volume", "Cubic Meters", "m³")

TeslaMeter = Unit.from_other_unit(Tesla*Meter, meaning="Motor strength")
MetersPerNewton = Unit.from_other_unit(Meter/Newton, meaning="Compliance")
NewtonSecondPerMeter = Unit.from_other_unit(Newton*Second/Meter, meaning="Mechanical resistance")
KiloPerSecond = Unit.from_other_unit(Kilogram / Second, meaning="Mechanical resistance")

# Subunits
MilliHenry = Unit.from_other_unit(Henry, name="milliHenry", symbol="mH", factor=1e-3)
Cm2 = Unit.from_other_unit(Meter2, name="square centimeters", symbol="cm²", factor=1e-4)
Gram = Unit.from_other_unit(Kilogram, name="gram", symbol="g", factor=1e-3)
Liter = Unit.from_other_unit(Meter3, name="liter", symbol="L", factor=1e-3)
MillimeterPerNewton = Unit.from_other_unit(MetersPerNewton, name="millimeters per Newton", symbol="mm/N", factor=1e-3)

NoUnit = Unit("Dimensionless parameter", "", "-")
