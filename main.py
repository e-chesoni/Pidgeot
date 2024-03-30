import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

from util.uav_logger import *
from src.settings import *
from util.helpers import *
from src.aircraft import *
from src.setup import *

from simulations.hw4.run import *
from simulations.hw5.run import *
from simulations.hw6.run import *

print("\n")
msg = "Welcome to UAV Sim!"
print(msg)
print("\n")

# TODO: Test imports
logging.info('Logging enabled')
logging.info(f"Log level: {logging.getLogger().getEffectiveLevel()}")

# Set Matplotlib logging level to suppress debug logs
logging.getLogger('matplotlib').setLevel(logging.WARNING)

run_hw4_simulation()
#run_hw5_simulation()
run_hw6_simulation()

'''
CD0 and K
-------------------------------------------------
Super Cub
Cd0: 0.020276808012452317, K: 0.07113059297128425

Highway Pursuit
CL_max: 0.8755367365454562
Cd0: 0.023116064306782497, K: 0.09090243378951311

Highway Pursuit With Flap
CL_max: 0.9589159267539666
Cd0: 0.024300075421965526, K: 0.1123014244759195
'''