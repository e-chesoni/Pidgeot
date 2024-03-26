import math
from src.NACA import NACA
from src.aerofoil import *

class Wing(Aerofoil):
    def __init__(self) -> None:
        pass

    # Setters
    def set_center_of_gravity(self, h_cg):
        self._h_cg = h_cg

    # Getters    
    def get_center_of_gravity(self):
        return self._h_cg
    
    # Finders
    # NOTE: use to be find_CL_wing
    def find_CL_NACA(self, alpha): # typical range for alpha values in radians: 0 - 0.1
        return self._NACA.find_CL(alpha)

    def find_CM(self, h): 
        return self._NACA._CM_aero_center + ((h - self._h_cg) * self._NACA._CL)