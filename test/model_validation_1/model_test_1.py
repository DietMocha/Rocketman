import matplotlib.pyplot as plt
import numpy as np
import math, rocket, planets

fire = rocket.Rocket(31, 90, time_step=0.0625, altitude=22000, propellant_mass_fraction=0.80, mixture_ratio=7.4, tank_pressure=7e6, tank_safety_factor=1.2)    # Initialize your rocket with design parameters and starting conditions
initial_mass = fire.vehicle.mass.total
fire.calc(150)    # Method's parameter is the length of simulation in seconds
final_mass = fire.vehicle.mass.total
exhaust_velocity = fire.engine.exhaust_velocity

Theorectical_Delta_V = exhaust_velocity * math.log(initial_mass / final_mass)
Model_Delta_V = fire.log[-1][2]

print('Theorectical Delta-V: ' + str(Theorectical_Delta_V) + ' m/s')
print('Model Delta-V: ' + str(Model_Delta_V) + ' m/s')
relative_error = (math.fabs(Theorectical_Delta_V - Model_Delta_V) / Theorectical_Delta_V) * 100
print('Relative Error: ' + str(round(relative_error, 4)) + '%')