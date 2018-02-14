import math, planets, csv

class Rocket(object):
	""" Describes a 1-stage rocket vehicle and start conditions. Use METRIC units. """
	def __init__(self, mass, burn_time, start_time=0, flight_time=120, time_step=0.0625, propellant_mass_fraction=0.87, 
		         altitude=0, velocity_radial=0, velocity_tangential=0, fuel='RP-1', oxidizer='H2O2_98%', 
		         mixture_ratio=5, g_limit=None, number_of_thrusters=1, feed_system='pressure-fed', 
		         tank_pressure=0, tank_material='Al_6061_T6', tank_safety_factor=2, drag_coefficent=0.30,
				 angle=0, turn_rate=5, exhaust_velocity=3250):
		self.step = time_step    # Time increment per iteratin | lower values increases the result's resolution | beware of roundoff error
		self.log = []    # Stores flight information
		self.time = start_time    # Rocket start time
		self.vehicle = Vehicle(mass, propellant_mass_fraction, mixture_ratio, burn_time, 
							   tank_material, fuel, oxidizer, tank_safety_factor, tank_pressure, 
							   drag_coefficent, g_limit)
		self.position = Position(altitude, angle)
		self.velocity = Velocity(velocity_radial, velocity_tangential, altitude)
		self.acceleration = Acceleration()
		self.engine = Engine(number_of_thrusters, feed_system, exhaust_velocity)
		self.air = Air()    # Atmospheric information

	def calc(self, calc_time):
		for _ in range(int(calc_time / self.step)):
			update_air(self)
			update_mass(self)
			calc_forces(self)
			calc_acceleration(self)
			calc_velocity(self)
			calc_position(self)
			self.time += self.step
			self.log.append([self.time, self.position.altitude, self.velocity.radial, self.acceleration.radial, self.thrust, self.drag, 
				             self.vehicle.mass.total, self.acceleration.tangential, self.velocity.tangential, self.velocity.total,
				             self.acceleration.total, self.position.horizontal, self.position.theta])

class Vehicle(object):
	def __init__(self, mass, propellant_mass_fraction, mixture_ratio, burn_time, tank_material, fuel, oxidizer, tank_safety_factor, 
		         tank_pressure, drag_coefficent, g_limit):
		self.mass = Mass(mass, propellant_mass_fraction, mixture_ratio)
		self.oxidizer_volume = self.mass.oxidizer / oxidizer_density[oxidizer]
		self.fuel_volume = self.mass.fuel / fuel_density[fuel]
		self.oxidizer_sphere_radius = ((3 * self.oxidizer_volume) / (4 * math.pi) ) ** (1.0 / 3.0)
		self.fuel_sphere_radius = ((3 * self.fuel_volume) / (4 * math.pi)) ** (1.0 / 3.0)
		self.frontal_area_sphere = (math.pi * (self.oxidizer_sphere_radius ** 2) if self.oxidizer_sphere_radius > self.fuel_sphere_radius else (math.pi * (self.fuel_sphere_radius ** 2)))
		self.oxidizer_wall_thickness = tank_safety_factor * (tank_pressure * self.oxidizer_sphere_radius / (2 * material[tank_material][0]))
		self.fuel_wall_thickness = tank_safety_factor * (tank_pressure * self.fuel_sphere_radius / (2 * material[tank_material][0]))
		self.oxidizer_mass = (4 * math.pi / 3) * (self.oxidizer_sphere_radius ** 3 - (self.oxidizer_sphere_radius - self.oxidizer_wall_thickness) ** 3) * material[tank_material][1]
		self.fuel_mass = (4 * math.pi / 3) * (self.fuel_sphere_radius ** 3 - (self.fuel_sphere_radius - self.fuel_wall_thickness) ** 3) * material[tank_material][1]
		self.oxidizer_flow_rate = self.mass.oxidizer / burn_time    # kg/s
		self.fuel_flow_rate = self.mass.fuel / burn_time    # kg/s
		self.drag_coefficent = drag_coefficent
		self.g_limit = g_limit

class Mass(Vehicle):
	def __init__(self, mass, propellant_mass_fraction, mixture_ratio):
		# Mass calulation needs to incorporate tank mass based on tank pressure
		self.total = mass    # Rocket's mass at launch
		self.propellant_fraction = propellant_mass_fraction    # 1 - dry weight at launch / fueled weight at launch
		self.dry = (1 - self.propellant_fraction) * self.total
		self.propellant = self.total - self.dry
		self.oxidizer = (mixture_ratio * self.propellant) / (mixture_ratio + 1)
		self.fuel = self.propellant / (mixture_ratio + 1)
		self.residual_fuel = mass*propellant_mass_fraction * 0.02   # Needs development, assuming 2% residual (unused fuel)

class Position(object):
	def __init__(self, altitude, angle):
		self.altitude = altitude    # Initial height above the surface, meters
		self.horizontal = 0    # Arc distance travelled down range
		self.theta = 0    # Arc angle created between the current position, the center of the Earth, and the starting position
		self.angle = angle * (math.pi / 180)    # Takes angle in degrees and converts it to radians | Zero degrees means the rocket is pointing away from the center of the Earth and aligned with the radial axis | pi/2 radians is when the rocket is aligned with the tangential axis

class Velocity(object):
	def __init__(self, velocity_radial, velocity_tangential, altitude):
		self.radial = velocity_radial
		self.tangential = velocity_tangential + (Earth.velocity_angular * (Earth.radius + altitude))    # Assume a stationary position over ground launch site if rocket is launched from a balloon
		self.total = (self.radial ** 2 + self.tangential ** 2) ** 0.5

class Acceleration(object):
	def __init__(self):
		self.radial = 0
		self.tangential = 0
		self.total = (self.radial ** 2 + self.tangential ** 2) ** 0.5

class Air(object):
	def __init__(self):    # Outside air conditions
		self.temperature = 0    # Celsius
		self.pressure = 0    # kPa
		self.density = 0    # kg/m3

class Engine(object):
	def __init__(self, number_of_thrusters, feed_system, exhaust_velocity):
		self.thrusters = number_of_thrusters    # The number of rocket engines in this stage
		self.feed_system = feed_system
		self.exhaust_velocity = exhaust_velocity    # Needs to be developed

def update_air(self):
	# NASA atmospheric model | https://www.grc.nasa.gov/www/k-12/rocket/atmosmet.html
	if self.position.altitude >=0 and self.position.altitude < 11000:
		self.air.temperature = 15.04 - .00649 * self.positon.altitude    # Celsius
		self.air.pressure = 101.29 * ((self.air.temperature + 273.1) / 288.08) ** 5.256    # kPa
	elif self.position.altitude >= 11000 and self.position.altitude <25000:
		self.air.temperature = -56.46    # Celsius
		self.air.pressure =  22.65 * math.exp(1.73 - 0.000157 * self.position.altitude)    # kPa
	elif self.position.altitude >= 25000:
		self.air.temperature = -131.21 + .00299 * self.position.altitude    # Celsius
		self.air.pressure = 2.488 * ((self.air.temperature + 273.1) / 216.6) ** -11.388    # kPa
	else:
		self.position.altitude = -0.1
	self.air.density = self.air.pressure / (0.2869 * (self.air.temperature + 273.1))    # kg/m3

def update_mass(self):
	# Calculate mass change based on fuel & oxidizer consumption rate
	if self.vehicle.mass.propellant > self.vehicle.mass.residual_fuel:    # Prevents mass reduction after rocket uses all available fuel
		self.vehicle.mass.oxidizer -= self.vehicle.oxidizer_flow_rate * self.step
		self.vehicle.mass.fuel -= self.vehicle.fuel_flow_rate * self.step
		self.vehicle.mass.propellant = self.vehicle.mass.oxidizer + self.vehicle.mass.fuel
		self.vehicle.mass.total = self.vehicle.mass.dry + self.vehicle.mass.propellant

def calc_forces(self):
	self.g = 9.805 * (Earth.radius / (self.position.altitude + Earth.radius)) ** 2    # Calculate Earth's gravitional constant base on altitude		
	self.thrust = (self.vehicle.oxidizer_flow_rate + self.vehicle.fuel_flow_rate) * self.engine.exhaust_velocity  if self.vehicle.mass.propellant > self.vehicle.mass.residual_fuel else 0    # Calculate rocket's thrust based on fuel & oxidizer consumption rate and gas exhaust velocity
	# Calculate rocket's drag based on vehicle's velocity relative to the surrounding air, velocity, drag coefficent, air denisty, and rocket's frontal area
	drag_velocity = ((self.velocity.tangential - Earth.velocity_angular * Earth.radius) ** 2 + self.velocity.radial ** 2) ** 0.5    # Velocity that contributes to drag | Vehicle's velocity relative to the surrounding air
	self.drag = (0.5 * self.vehicle.drag_coefficent * self.air.density * drag_velocity**2 * self.vehicle.frontal_area_sphere) if self.position.altitude <= 80000 else 0

def calc_acceleration(self):
	# Calculate rocket's acceleration based on froces and then split the result into radial and tangential components (center of Earth is the reference point | the plane is Earth's equator)
	rocket_acceleration = (self.thrust - self.drag) / self.vehicle.mass.total
	self.acceleration.radial = rocket_acceleration * math.cos(self.position.angle) - self.g + (self.velocity.tangential ** 2 / (self.position.altitude + Earth.radius))    # Radial acceleration from thrust - Earth's gravitational acceleration + centripetal acceleration
	self.acceleration.tangential = rocket_acceleration * math.sin(self.position.angle)
	self.acceleration.total = (self.acceleration.tangential ** 2 + self.acceleration.radial ** 2) ** 0.5

def calc_velocity(self):
	# Calculates rocket's velocity base on acceleration in radial and tangential coordinates
	self.velocity.radial += self.acceleration.radial * self.step
	self.velocity.tangential += self.acceleration.tangential * self.step
	self.velocity.total = (self.velocity.radial ** 2 + self.velocity.tangential ** 2) ** 0.5

def calc_position(self):
	self.position.altitude += self.velocity.radial * self.step    # Height above surface
	self.position.horizontal += (self.velocity.tangential - Earth.velocity_angular * (Earth.radius + self.position.altitude)) * self.step    # Horizontal distance from start location
	self.position.theta += math.atan(self.velocity.tangential * self.step) / (self.position.altitude + Earth.radius)    # Radians

Earth = planets.Earth()    # Planet reference information

# Reference dictionaries
oxidizer_density = {'H2O2_98%': 1430}    # kg/m3
fuel_density = {'RP-1': 810}    # kg/m3
material = {'Al_6061_T6': [240e6, 2700]}   # { name: [yield strength (Pa), density (kg/m3)] }

# NOTES
# Looking into the burn time. I believe the residual fuel shortens the burn time by a few seconds.
# Time step of 0.0625 seconds yielded the best results when the model was compared to the rocket equation
# Improve model's direction of flight angle vs rocket's angle of attack. At this moment, they are the same. In reality, this is not the case
# Need to improve rocket's mass prediction based on tank pressure