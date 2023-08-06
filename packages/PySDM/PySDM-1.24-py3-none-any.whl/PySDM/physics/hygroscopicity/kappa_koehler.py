"""
kappa-Koehler parameterization
 ([Petters & Kreidenweis 2007](https://doi.org/10.5194/acp-7-1961-2007))
"""
from numpy import sqrt, exp
import PySDM.physics.constants as const


class KappaKoehler:
    @staticmethod
    def RH_eq(r, T, kp, rd3, sgm):
        return exp(
            (2 * sgm / const.Rv / T / const.rho_w) / r
        ) * (r**3 - rd3) / (r**3 - rd3 * (1-kp))

    @staticmethod
    def r_cr(kp, rd3, T, sgm):
        # TODO #493
        return sqrt(3 * kp * rd3 / (2 * sgm / const.Rv / T / const.rho_w))
