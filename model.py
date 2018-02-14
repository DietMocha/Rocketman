import matplotlib.pyplot as plt
import numpy as np
import math, rocket, planets

def burn_angle_optimize():
	for burn_time in range(40, 100, 5):
		print('Burn time: ' + str(burn_time))
		for launch_angle in range(50, 65, 1):
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

def single_test(weight):
	fire = rocket.Rocket(weight, 75, altitude=22000, propellant_mass_fraction=0.80, mixture_ratio=7.4, tank_pressure=7e6, tank_safety_factor=1.2, angle=55)    # Initialize your rocket with design parameters and starting conditions
	fire.calc(50)    # Method's parameter is the length of simulation in seconds

	time = [row[0] for row in fire.log]
	altitude = [row[1] / 1000 for row in fire.log]
	print(str(weight) + '\t' + str(int(round(max(altitude), 0))) + 'km')
	velocity_radial = [row[2] for row in fire.log]
	velocity_tangential = [row[8] for row in fire.log]
	velocity_total = [row[9] for row in fire.log]
	acceleration_radial = [row[3] / 9.805 for row in fire.log]    # Unit converted from m/s2 to G's
	acceleration_tangential = [row[7] / 9.805 for row in fire.log]
	acceleration_total = [row[10] / 9.805 for row in fire.log]
	thrust = [row[4] for row in fire.log]
	drag = [row[5] for row in fire.log]
	mass = [row[6] for row in fire.log]
	horizontal = [row[11] / 1000 for row in fire.log]    # Units converted from m to km
	theta = [row[12] for row in fire.log]

	f, ax = plt.subplots(2, 5)

	ax[0, 0].scatter(time, altitude)
	ax[0, 0].set_title('Altitude [km]')
	plt.xlabel('time [s]')

	ax[0, 1].scatter(time, velocity_radial)
	ax[0, 1].set_title('Radial Velocity [m/s]')
	plt.xlabel('time [s]')

	ax[0, 2].scatter(time, velocity_tangential)
	ax[0, 2].set_title('Tangential Velocity [m/s]')
	plt.xlabel('time [s]')

	ax[0, 3].scatter(time, velocity_total)
	ax[0, 3].set_title('Total Velocity [m/s]')
	plt.xlabel('time [s]')

	ax[0, 4].scatter(time, horizontal)
	ax[0, 4].set_title('Horizontal arc distance traveled [km]')
	plt.xlabel('time [s]')

	ax[1, 0].scatter(time, acceleration_total)
	ax[1, 0].set_title('Acceleration [g]')
	plt.xlabel('time [s]')

	ax[1, 2].scatter(time, thrust)
	ax[1, 2].set_title('Thrust [N]')
	plt.xlabel('time [s]')

	ax[1, 3].scatter(time, drag)
	ax[1, 3].set_title('Drag [N]')
	plt.xlabel('time [s]')

	ax[1, 4].scatter(time, theta)
	ax[1, 4].set_title('Theta [deg]')
	plt.xlabel('time [s]')
	
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()

# burn_angle_optimize()

# for weight in range(500, 2000, 100):
single_test(100)