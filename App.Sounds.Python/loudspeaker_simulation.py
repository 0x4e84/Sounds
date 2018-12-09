from loudspeakers.Loudspeaker import Loudspeaker
from loudspeakers.Enclosure import Enclosure
from loudspeakers.Unit import *

tang_band_ws1138smf = Loudspeaker("Tang Band", "W5-1138SMF")
tang_band_ws1138smf.set_ts_parameters(re=3.5, le=1.0e-3, fs=33.0, qms=2.2, qes=0.46, qts=0.38)
# tang_band_ws1138smf.set_fundamental_parameters(sd=82.0, mms=22.0, cms=1.1, rms=22.0, vas=10.0, bl=5.9)
tang_band_ws1138smf.Sd.set_value(82.0, Cm2)
tang_band_ws1138smf.Mms.set_value(22.0, Gram)
tang_band_ws1138smf.Cms.set_value(1.1, MillimeterPerNewton)
tang_band_ws1138smf.Rms.set_value(22.0, KiloPerSecond)
tang_band_ws1138smf.Vas.set_value(10.0, Liter)
tang_band_ws1138smf.Bl.set_value(5.9, TeslaMeter)
print()

tang_band_ws1138smf.compute_qts()
tang_band_ws1138smf.compute_fs()
print()

sealed_box = Enclosure("Box1", "Sealed Box", "Sealed")
sealed_box.set_inner_dimensions(0.6, 0.4, 0.4)
