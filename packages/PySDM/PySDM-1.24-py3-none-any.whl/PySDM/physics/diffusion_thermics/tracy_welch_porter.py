"""
based on "PROPERTIES OF AIR: A Manual for Use in Biophysical Ecology"
(Fourth Edition - 2010, page 22)
"""
from numpy import power
from PySDM.physics import constants as const


class TracyWelchPorter:
    @staticmethod
    def D(T, p):
        return const.D0 * power(T / const.T0, const.D_exp) * (const.p1000 / p)
