import matplotlib.pyplot as plt
import numpy as np
import rocket, planets

# Initialize your rocket with design parameters and starting conditions
vehicle = rocket.Rocket(310, 90, time_step=0.1, altitude=22000, propellant_mass_fraction=0.80, mixture_ratio=7.4, tank_pressure=7e6, tank_safety_factor=1.2)

# Run model
vehicle.calc(2000)    # Method's parameter is the length of simulation in seconds

# Extract data from flight log
time = [row[0] for row in vehicle.log]
altitude = [row[1] for row in vehicle.log]
velocity_radial = [row[2] for row in vehicle.log]
acceleration_radial = [row[3] / 9.805 for row in vehicle.log]    # Unit converted from m/s2 to G's
thrust = [row[4] for row in vehicle.log]
drag = [row[5] for row in vehicle.log]
mass = [row[6] for row in vehicle.log]

# weights = range(20, 500, 10)
# height_weight_lst = []

# for weight in weights:
# 	fire = rocket.Rocket(weight, 120, time_step=0.1, altitude=22000, propellant_mass_fraction=0.80, mixture_ratio=7.4, tank_pressure=7e6, tank_safety_factor=1.2)
# 	fire.calc(120)
# 	altitude = [row[1] for row in fire.log]
# 	height_weight_lst.append([weight, max(altitude)])

# height_weight_lst = np.array(height_weight_lst)
# f, ax = plt.subplots(1, 1)
# ax.scatter(height_weight_lst[:, 0], height_weight_lst[:, 1])
# plt.show()

# Plot results
f, ax = plt.subplots(2, 3)

ax[0, 0].scatter(time, altitude)
ax[0, 0].set_title('Altitude [m]')

ax[0, 1].scatter(time, velocity_radial)
ax[0, 1].set_title('Radial Velocity [m/s]')

ax[0, 2].scatter(time, drag)
ax[0, 2].set_title('Drag [N]')

ax[1, 0].scatter(time, acceleration_radial)
ax[1, 0].set_title('Radial Acceleration [g]')

ax[1, 1].scatter(time, thrust)
ax[1, 1].set_title('Thrust [N]')

ax[1, 2].scatter(time, mass)
ax[1, 2].set_title('Mass [kg]')

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
plt.show()