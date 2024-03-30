import math
import numpy as np

def in_to_meters(value):
    return value/39.37

def ft_to_meters(value):
    return value/3.281

def deg_to_rad(value):
    return value * (math.pi / 180)

def kg_to_g(value):
    return value / 1000

def rpm_to_rads(rpm):
    return rpm * 2 * np.pi / 60

def rads_to_rpm(rps):
    return (rps * 60) / (2 * np.pi)