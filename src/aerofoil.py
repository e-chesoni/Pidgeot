import math

from util.helpers import *
from src.NACA import *

class Aerofoil:
    def __init__(self) -> None:
        self._NACA = None
        self._span = None
        self._chord = None
        self._thickness = None
        self._h_cg = None  # Center of gravity might be more specific to wings, consider if it should be here

    # Setters
    def set_span_m(self, n):
        self._span = n
    
    def set_chord_m(self, n):
        self._chord = n
    
    def set_thicknes_m(self, n):
        self._thickness = n
    
    def set_NACA(self, NACA):
        self._NACA = NACA
    
    def set_NACA_from_data(self, naca_value, naca_data):

        naca_params = naca_data[f"NACA_{naca_value}"]

        Cd = naca_params["Cd"]
        Cd0 = naca_params["Cd0"]
        CL = naca_params["CL"]
        alpha_0_deg = naca_params["alpha_0_deg"]
        CL_start = naca_params["CL_start"]
        CL_end = naca_params["CL_end"]
        alpha_start_deg = naca_params["alpha_start_deg"]
        alpha_end_deg = naca_params["alpha_end_deg"]
        e = naca_params["e"]

        
        naca = NACA(naca_value, Cd, CL, Cd0, deg_to_rad(alpha_0_deg), self.get_AR(), e)
        naca.set_CL_window(CL_start, CL_end)
        naca.set_alpha_window(alpha_start_deg, alpha_end_deg)
        naca.set_CM_aero_center(naca_params["CMac"])
        
        self.set_NACA(naca)

    # Getters
    def get_span_m(self):
        return self._span
    
    def get_chord_m(self):
        return self._chord
    
    def get_thickness_m(self):
        return self._thickness
    
    def get_AR(self):
        return self._span / self._chord
    
    def get_NACA(self):
        return self._NACA
    
    # Common calculations
    # TODO: Is this formula correct?
    def find_CD_NACA(self):
        return self._NACA.find_CD()
    
    def find_CD(self, CL):
        return self.get_NACA()._Cd0 + (self.get_NACA().get_r() * (CL**2)) + ((CL**2) / (math.pi * self.get_NACA()._e * self.get_NACA()._AR))
    
    # Export vairables
    def export_variables_to_dict(self):
        """
        Exports Aerofoil variables to a dictionary.
        """
        return {
            "Span": self._span,
            "Chord": self._chord,
            "Thickness": self._thickness,
            "Center of Gravity": self._h_cg
        }
    