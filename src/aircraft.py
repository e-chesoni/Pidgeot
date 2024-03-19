from src.wing import *
from src.tail import *
from src.fuselage import *

from collections import namedtuple

class Aircraft:
    def __init__(self, name, wing, tail, fuselage):
        self._name = name
        self._wing = wing
        self._tail = tail
        self._fuselage = fuselage

    # Setters
    def set_i_h(self, i_h):
        self._i_h = i_h

    def set_wing_surface_area_in(self, wing_surface_area_in):
        self._wing_surface_area_in = wing_surface_area_in
    
    def set_tail_surface_area_in(self, tail_surface_area_in):
        self._tail_surface_area_in = tail_surface_area_in
    
    def set_wing_chord_in(self, wing_chord_in):
        self._wing_chord_in = wing_chord_in
    
    # Simulation Methods
    def simulate(self, alpha_deg, del_e_deg, Re_c, h):
        AeroCoefficients = namedtuple('AeroCoefficients', 'CL CD CM')
        
        # WING
        CL_wing = self._wing.find_CL_NACA(deg_to_rad(alpha_deg))
        CD_wing = self._wing.find_CD_NACA()
        CM_wing = self._wing.find_CM(h)

        # TAIL
        CL_tail = self._tail.find_CL(deg_to_rad(alpha_deg), deg_to_rad(del_e_deg), self._i_h)
        CD_tail = self._tail.find_CD_NACA()
        CM_tail = self._tail.find_CM(in_to_meters(self._tail_surface_area_in), in_to_meters(self._wing_surface_area_in), in_to_meters(self._wing_chord_in), CL_tail)

        # FUSELAGE
        CD_fuselage = self._fuselage.find_CD(Re_c, in_to_meters(self._wing_chord_in))
        # NOTE: adjust super_cub_fuselage volume by * 1/3 for taper
        volume_taper_percent = (1/3)
        CM_fuselage = self._fuselage.find_CM(deg_to_rad(alpha_deg), in_to_meters(self._wing_surface_area_in), in_to_meters(self._wing_chord_in), volume_taper_percent)

        CL = CL_wing + CL_tail
        CD = CD_wing + CD_tail + CD_fuselage
        CM = CM_wing + CM_tail + CM_fuselage
        
        # NOTE: PAY ATTENTION TO RETURN ORDER HERE!!
        return AeroCoefficients(CL=CL, CD=CD, CM=CM)
