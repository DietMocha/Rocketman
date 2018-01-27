import math, planets

Earth = planets.Earth()

oxidizer_density = {'H2O2_98%': 1430}    # kg/m3
fuel_density = {'RP-1': 810}    # kg/m3
material = {'Al_6061_T6': [240e6, 2700]}   # name: [yield strength (Pa), density (kg/m3)]

class Rocket(object):
	""" Describes a 1-stage rocket vehicle and start conditions. Use metric units. """

	def __init__(self, mass, propellant_mass_fraction=0.87, altitude=0, radial_velocity=0,
				 angular_velocity=0, fuel='RP-1', oxidizer='H2O2_98%', mixture_ratio=5, g_limiter=6, isp=0,
				 number_of_thrusters=1, feed_system='pressure-fed', tank_pressure=0, tank_material='Al_6061_T6',
				 tank_safety_factor=2):

		# Starting conditions
		self.radius = altitude + Earth.radius
		self.radial_velocity = radial_velocity
		self.angular_velocity = angular_velocity + Earth.angular_velocity

		# Mass
		self.mass = mass    # Rocket's mass at launch
		self.propellant_mass_fraction = propellant_mass_fraction    # 1 - dry weight at launch / fueled weight at launch
		self.dry_mass = -(self.propellant_mass_fraction - 1) * self.mass
		self.propellant_mass = self.mass - self.dry_mass
		self.oxidizer_mass = (mixture_ratio * self.propellant_mass) / (mixture_ratio + 1)
		self.fuel_mass = self.propellant_mass / (mixture_ratio + 1)

		# Engine
		self.fuel = fuel
		self.oxidizer = oxidizer
		self.mixture_ratio = mixture_ratio    # Oxidizer mass / fuel mass
		self.isp = isp    # Rocket engine's specific impulse, e.g. 285 seconds
		self.number_of_thrusters = number_of_thrusters    # The number of rocket engines in this stage
		self.feed_system = feed_system
		self.tank_pressure = tank_pressure    # Pa
		self.tank_safety_factor = tank_safety_factor

		# Tanks
		self.oxidizer_volume = self.oxidizer_mass / oxidizer_density[oxidizer]
		self.fuel_volume = self.fuel_mass / fuel_density[fuel]
		self.oxidizer_tank_radius_sphere = ( (3*self.oxidizer_volume) / (4*math.pi) ) ** (1.0 / 3.0)
		self.fuel_tank_radius_sphere = ( (3*self.fuel_volume) / (4*math.pi) ) ** (1.0 / 3.0)
		self.oxidizer_tank_wall_thickness = 0
		self.fuel_tank_wall_thickness = 0

		# Limitations
		self.g_limiter = g_limiter    # Limits the amount of g forces can experience


rocket = Rocket(31, propellant_mass_fraction=0.80, mixture_ratio=7.4)

print(rocket.oxidizer_volume)
print(rocket.oxidizer_tank_radius_sphere)
print(rocket.fuel_volume)
print(rocket.fuel_tank_radius_sphere)