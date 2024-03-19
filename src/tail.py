import math
from src.NACA import *
from src.aerofoil import *

class Tail(Aerofoil):
    def __init__(self) -> None:
        pass
    
    # Setters
    def set_tail_thickness(self, n):
        self._tail_thickness = n
    
    def set_epsilon(self, epsilon):
        self._epsilon = epsilon
    
    def set_tau(self, tau):
        self._tau = tau

    def set_moment_arm_length(self, moment_arm_tail):
        self._moment_arm = moment_arm_tail
    
    # Getters
    def get_elevator_chord(self):
        return self._elevator_chord

    def get_tail_thickness(self):
        return self._tail_thickness
    
    def get_epsilon(self):
        return self._epsilon
    
    def get_tau(self):
        return self._tau

    # Calculations
    def find_volume(self, l, S, S_wing, chord_wing):
        return (l * S) / (S_wing * chord_wing)

    def find_epsilon(self, CL_wing, e_tail, AR_wing):
        return (2 * CL_wing) / (math.pi * e_tail * AR_wing)

    # NOTE: Cet/CLt = 0.2/0.5
    # NOTE: use find_epsilon before this function
    def find_CL(self, alpha_test_rad, del_e_rad, i_h):
        return self._NACA.find_a3D() * (alpha_test_rad + (self.get_tau() * del_e_rad) - self.get_epsilon() + i_h)
    
    def find_CM(self, surface_area_tail, surface_area_wing, chord_wing, CL_tail):
        return (-self.find_CV(surface_area_tail, surface_area_wing, chord_wing)) * CL_tail

    # Tail Volume Coefficient
    def find_CV(self, surface_area_tail, surface_area_wing, chord_wing):
        return (self._moment_arm * surface_area_tail) / (surface_area_wing * chord_wing)