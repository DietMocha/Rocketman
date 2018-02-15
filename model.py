import matplotlib.pyplot as plt
import numpy as np
import math
import rocket
import planets

position_parms = {
    'altitude': 22000,
    'angle': 0
}
velocity_parms = {
    'velocity_radial': 0,
    'velocity_tangential': 0,
    'altitude': position_parms['altitude']
}
acceleration_parms = {
    'acceleration_radial': 0,
    'acceleration_tangential': 0
}
engine_parms = {
    'exhaust_velocity': 3240
}
vehicle_parms = {
    'mass': 1000,
    'propellant_mass_fraction': 0.80,
    'mixture_ratio': 5,
    'burn_time': 60,
    'tank_material': 'Al_6061_T6',
    'fuel': 'RP-1',
    'oxidizer': 'H2O2_98%',
    'tank_safety_factor': 2,
    'tank_pressure': 0,
    'drag_coefficent': 0.32
}

position = rocket.Position(**position_parms)
velocity = rocket.Velocity(**velocity_parms)
acceleration = rocket.Acceleration(**acceleration_parms)
engine = rocket.Engine(**engine_parms)
vehicle = rocket.Vehicle(**vehicle_parms)
fire = rocket.Rocket(position, velocity, acceleration, engine, vehicle)
fire.calc(50)

fire.plotter()
plt.show()
