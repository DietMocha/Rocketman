import matplotlib.pyplot as plt
import numpy as np
import math, rocket, planets

for burn_time in range(40, 100, 5):
	print('Burn time: ' + str(burn_time))
	for launch_angle in range(0, 80, 5):
		try:
			fire = rocket.Rocket(31, burn_time, altitude=22000, propellant_mass_fraction=0.80, mixture_ratio=7.4, tank_pressure=7e6, tank_safety_factor=1.2, angle=launch_angle)    # Initialize your rocket with design parameters and starting conditions
			fire.calc(burn_time)    # Method's parameter is the length of simulation in seconds

			time = [row[0] for row in fire.log]
			altitude = [row[1] / 1000 for row in fire.log]
			velocity_radial = [row[2] for row in fire.log]
			velocity_tangential = [row[8] for row in fire.log]
			print('Launch angle: ' + str(launch_angle) + ' \tvelocity_tangential: ' + str(round(max(velocity_tangential), 0)) + 
				  ' \t altitude: ' + str(round(max(altitude), 0)) + 'km')
			velocity_total = [row[9] for row in fire.log]
			acceleration_radial = [row[3] / 9.805 for row in fire.log]    # Unit converted from m/s2 to G's
			acceleration_tangential = [row[7] / 9.805 for row in fire.log]
			thrust = [row[4] for row in fire.log]
			drag = [row[5] for row in fire.log]
			mass = [row[6] for row in fire.log]
		except:
			pass
# f, ax = plt.subplots(2, 4)

# ax[0, 0].scatter(time, altitude)
# ax[0, 0].set_title('Altitude [km]')
# plt.xlabel('time [s]')

# ax[0, 1].scatter(time, velocity_radial)
# ax[0, 1].set_title('Radial Velocity [m/s]')
# plt.xlabel('time [s]')

# ax[0, 2].scatter(time, velocity_tangential)
# ax[0, 2].set_title('Tangential Velocity [m/s]')
# plt.xlabel('time [s]')

# ax[0, 3].scatter(time, velocity_total)
# ax[0, 3].set_title('Total Velocity [m/s]')
# plt.xlabel('time [s]')

# ax[1, 0].scatter(time, acceleration_radial)
# ax[1, 0].set_title('Radial Acceleration [g]')
# plt.xlabel('time [s]')

# ax[1, 1].scatter(time, acceleration_tangential)
# ax[1, 1].set_title('Tangential Acceleration [g]')
# plt.xlabel('time [s]')

# ax[1, 2].scatter(time, thrust)
# ax[1, 2].set_title('Thrust [N]')
# plt.xlabel('time [s]')

# ax[1, 3].scatter(time, drag)
# ax[1, 3].set_title('Drag [N]')
# plt.xlabel('time [s]')

# mng = plt.get_current_fig_manager()
# mng.resize(*mng.window.maxsize())
# plt.show()