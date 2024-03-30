import math


class Motor:
    def __init__(self, K, R, i_0) -> None: # Km, Rm, and i_0 are empirical constants
        self._K = K
        self._R = R
        self._i_0 = i_0

    # Calcs
    def calculate_omega(n): # n = rpm
        # omega is angular velocity in rev per second
        return (n * 2 * math.pi) / 60 # div by 60 b/c 60 sec in 1 min
    
    def calculate_omega(self, P, Q):
        return P / Q

    def calculate_motor_power(e, Km, Rm, i0, omega):
        return Km * ( ((e - (Km * omega)) / Rm) - i0 ) * omega
    
    def calculate_Q(self, i_curr):
        return self._K * (i_curr - self._i_0)