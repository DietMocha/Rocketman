import math, planets, csv

class Rocket(object):
	""" Describes a 1-stage rocket vehicle and start conditions. Use METRIC units [kg, m, s, Pa, N, K]. """

	def __init__(self, mass, burn_time, flight_time=0, time_step=0.01, propellant_mass_fraction=0.87, altitude=0, velocity_radial=0,
				 velocity_angular=0, fuel='RP-1', oxidizer='H2O2_98%', mixture_ratio=5, g_limiter=None, isp=0,
				 number_of_thrusters=1, feed_system='pressure-fed', tank_pressure=0, tank_material='Al_6061_T6',
				 tank_safety_factor=2, drag_coefficent = 0.30):

		# Starting conditions
		self.flight_log = []
		self.flight_time = 0    # Rocket lifts-off at flight_time = 0 seconds
		self.time_step = time_step
		self.altitude = altitude    # Height above the surface
		# self.angle = 0    # The angle between the rocket and the launch site with respect to the Earth's center
		self.velocity_radial = velocity_radial
		self.velocity_angular = velocity_angular + Earth.velocity_angular
		self.velocity_total = (self.velocity_radial**2 + self.velocity_angular**2) ** 0.5
		self.acceleration_radial = 0
		# self.acceleration_angular = 
		# self.acceleration_total = (self.acceleration_radial**2 + self.acceleration_angular**2) ** 0.5
		self.g = 9.805 * (Earth.radius / (self.altitude + Earth.radius)) ** 2    # Earth's gravitational constant, which depends on altitude

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
		self.burn_time = burn_time    # How long are the engines ignited, in seconds?
		self.oxidizer_flow_rate = self.oxidizer_mass / burn_time    # kg/s
		self.fuel_flow_rate = self.fuel_mass / burn_time
		self.exhaust_velocity = 3250    # Needs to be developed
		self.thrust = (self.oxidizer_flow_rate + self.fuel_flow_rate) * self.exhaust_velocity    # Needs to be developed
		self.drag = 0

		# Tanks
		self.tank_pressure = tank_pressure    # Pa
		self.tank_safety_factor = tank_safety_factor
		self.tank_material = tank_material
		self.oxidizer_volume = self.oxidizer_mass / oxidizer_density[oxidizer]
		self.fuel_volume = self.fuel_mass / fuel_density[fuel]
		self.oxidizer_tank_radius_sphere = ( (3 * self.oxidizer_volume) / (4 * math.pi) ) ** (1.0 / 3.0)
		self.fuel_tank_radius_sphere = ( (3 * self.fuel_volume) / (4 * math.pi) ) ** (1.0 / 3.0)
		self.oxidizer_tank_wall_thickness = self.tank_safety_factor * (self.tank_pressure * self.oxidizer_tank_radius_sphere) / (2 * material[self.tank_material][0])
		self.fuel_tank_wall_thickness = self.tank_safety_factor * (self.tank_pressure * self.fuel_tank_radius_sphere) / (2 * material[self.tank_material][0])
		self.oxidizer_tank_mass = (4 * math.pi / 3) * (self.oxidizer_tank_radius_sphere ** 3 - (self.oxidizer_tank_radius_sphere - self.oxidizer_tank_wall_thickness) ** 3) * material[self.tank_material][1]
		self.fuel_tank_mass = (4 * math.pi / 3) * (self.fuel_tank_radius_sphere ** 3 - (self.fuel_tank_radius_sphere - self.fuel_tank_wall_thickness) ** 3) * material[self.tank_material][1]

		# Deign
		self.drag_coefficent = drag_coefficent
		self.frontal_area_sphere = (math.pi * (self.oxidizer_tank_radius_sphere) ** 2) if self.oxidizer_tank_radius_sphere > self.fuel_tank_radius_sphere else (math.pi * (fuel_tank_radius_sphere) ** 2)

		# Limitations
		self.g_limiter = g_limiter    # Limits the amount of g forces can experience

	def calc_g(self):
		self.g = 9.805 * (Earth.radius / (self.altitude + Earth.radius)) ** 2

	def calc_mass(self):
		self.oxidizer_mass -= self.oxidizer_flow_rate * self.time_step
		self.fuel_mass -= self.fuel_flow_rate * self.time_step
		self.propellant_mass = self.oxidizer_mass + self.fuel_mass
		self.mass = self.dry_mass + self.propellant_mass

	def calc_acceleration_radial(self):
		self.drag = 0.5 * self.drag_coefficent * atm_air_density[atm_height.index(round(self.altitude, -2))] * (self.velocity_radial)**2 * self.frontal_area_sphere
		self.acceleration_radial = ((self.thrust - self.drag) / self.mass) - self.g

	def calc_velocity_radial(self):
		self.velocity_radial += self.acceleration_radial * self.time_step

	def calc_altitude(self):
		self.altitude += self.velocity_radial * self.time_step

	def calc_time(self):
		self.flight_time += self.time_step

	def calc(self, time):
		for time_increment in range(int(time / self.time_step)):
			self.flight_log.append([self.flight_time, self.altitude, self.velocity_radial, self.acceleration_radial, self.thrust, self.drag, self.mass])
			self.calc_mass()
			self.calc_acceleration_radial()
			self.calc_velocity_radial()
			self.calc_altitude()
			self.calc_time()

# Loads the US Standard Atmosphere Table
# Needs improvements, only goes up to 80,000 meters and need to increase table's resolution
with open('US_standard_atmosphere.csv') as csvfile:
	std_atm = [row for row in csv.reader(csvfile, delimiter='\t')]    # Each row contains height above surface, temperature, pressure, density of air
atm_height = [float(row[0]) for row in std_atm]
atm_temperature = [float(row[1]) for row in std_atm]
atm_pressure = [float(row[2]) for row in std_atm]
atm_air_density = [float(row[3]) for row in std_atm]

# Planet reference information
Earth = planets.Earth()

# Reference dictionaries
oxidizer_density = {'H2O2_98%': 1430}    # kg/m3
fuel_density = {'RP-1': 810}    # kg/m3
material = {'Al_6061_T6': [240e6, 2700]}   # name: [yield strength (Pa), density (kg/m3)]