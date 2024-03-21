import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

from util.uav_logger import *
from util.helpers import *
from src.aircraft import *
from src.setup import *

from simulations.hw4 import *

print("\n")
msg = "Welcome to UAV Sim!"
print(msg)
print("\n")

# TODO: Test imports
logging.info('Logging enabled')
logging.info(f"Log level: {logging.getLogger().getEffectiveLevel()}")
print("\n")

run_hw4_simulation()