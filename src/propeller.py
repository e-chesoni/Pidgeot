from util.helpers import *

class Propeller:
    def __init__(self, d, Q, K, i, i_0) -> None:
        self._d = d
        self._Q = Q
        self._K = K
        self._i = i
        self._i_0 = i_0

    # Setters
    def set_diameter(self, d):
        self._diameter = d

    # Getters
    def get_Q(self):
        return self._K * (self._i * self._i_0)
    
    # Calculations
    def calculate_J(self, V, n_rpm):
        n_rads = rpm_to_rads(n_rpm)  # Convert RPM to rad/s
        n = n_rads / (2 * np.pi)  # Convert rad/s to rev/s
        J = V / (n * self._d)
        return J

    # Function to calculate thrust in grams
    def calculate_thrust(self, C_T, rho, n_rpm):
        n_rads = rpm_to_rads(n_rpm)
        n = n_rads / (2 * np.pi)
        T = C_T * rho * n**2 * self._d**4
        return T * 1000  # Convert to grams (1 N = 1000 grams)

    # Function to calculate power in Watts
    def calculate_power(self, C_P, rho, n_rpm):
        n_rads = rpm_to_rads(n_rpm)
        n = n_rads / (2 * np.pi)
        P = C_P * rho * n**3 * self._d**5
        return P

    def calcuate_rads_per_sec(self, T, rho, diameter, CT): # n
        return math.sqrt( T / (rho * (diameter**4) * CT) )

    def calculate_rpm(n):
        # TODO: call calc_n
        pass
