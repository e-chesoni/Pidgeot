import math

class Fuselage:
    def __init__(self) -> None:
        pass

    # Setters
    def set_length(self, l_meters):
        self._length = l_meters
    
    def set_height(self, h_meters):
        self._height = h_meters

    # Getters
    def get_length(self):
        return self._length
    
    def get_height(self):
        return self._height
    
    def get_d_to_l_ratio(self):
        # NOTE: height = diameter
        return (self._height / self._length)
    
    def get_volume(self):
        # NOTE: volume_cylinder = pi * radius^2 * height
        return (math.pi * ((self._height / 2)**2) * self._height)

    # Calculations
    def turbulant_CD(self):
        return (1.328 / 10**5) * ( (1 + (self.get_d_to_l_ratio() ** (3/2))) + (0.11 * (self.get_d_to_l_ratio() ** 2)) )

    def laminar_CD(self):
        return (0.074 / 10**2) * ( (1 + (1.5 * (self.get_d_to_l_ratio() ** (3/2)))) + (7 * (self.get_d_to_l_ratio() **2)) )
    
    def find_CD(self, Renyolds, chord_wing_m):
        lam_or_turb = ((self._length / chord_wing_m) * Renyolds)
        if (lam_or_turb > 10**5):
            return self.turbulant_CD()
        else:
            return self.laminar_CD()
    
    def find_CM(self, alpha, surface_area_wing_m, chord_wing_m, volume_taper_percent):
        return ( (2 * (volume_taper_percent * self.get_volume()) * alpha) / (surface_area_wing_m * chord_wing_m) )