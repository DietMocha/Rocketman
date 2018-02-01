import matplotlib.pyplot as plt
import numpy as np
import rocket, planets

def plotter(x, y, kind='scatter', title=None, x_label=None, y_label=None):
	f, ax = plt.subplots(1, 1)
	if kind == 'scatter':
		ax.scatter(x, y)
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()

def optimizer(mass_start, mass_end, mass_step, burn_time, flight_time=120, time_step=0.01, propellant_mass_fraction=0.87, altitude=0, velocity_radial=0,
			  velocity_tangential=0, fuel='RP-1', oxidizer='H2O2_98%', mixture_ratio=5, g_limit=None, number_of_thrusters=1, 
			  feed_system='pressure-fed', tank_pressure=0, tank_material='Al_6061_T6', tank_safety_factor=2, drag_coefficent=0.30,
			  angle=0, turn_rate=5, exhaust_velocity=3250):
	""" Recommend setting time_step to 0.1 seconds for initial optimization to reduce the runtime """
	height_mass_lst = []
	for mass in range(mass_start, mass_end, mass_step):
		vehicle = rocket.Rocket(mass, burn_time, flight_time, time_step, propellant_mass_fraction, altitude, velocity_radial,
				 				velocity_tangential, fuel, oxidizer, mixture_ratio, g_limit, number_of_thrusters, 
				 				feed_system, tank_pressure, tank_material, tank_safety_factor, drag_coefficent,
				 				angle, turn_rate, exhaust_velocity)
		vehicle.calc(flight_time)
		altitude = [row[1] for row in vehicle.flight_log]
		height_mass_lst.append([mass, max(altitude)])
	height_mass_lst = np.array(height_mass_lst)
	plotter(height_mass_lst[:, 0], height_mass_lst[:, 1], 'scatter', 'Initial Mass vs Final Altitude', 'Initial Mass [kg]', 'Final Altitude [m]')

# vehicle = rocket.Rocket(40, 120, time_step=0.1, altitude=22000, propellant_mass_fraction=0.80, mixture_ratio=7.4, tank_pressure=7e6, tank_safety_factor=1.2)
optimizer(40, 100, 10, 120, 500, time_step=0.1, altitude=22000, propellant_mass_fraction=0.80, mixture_ratio=7.4, tank_pressure=7e6, tank_safety_factor=1.2)