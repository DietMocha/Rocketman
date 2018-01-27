import planets

Earth = planets.Earth()

class Rocket(object):
	""" Describes the rocket vehicle and start conditions. Use metric units. """
	def __init__(self, mass, propellant_mass_fraction=0.87, altitude=0, radial_velocity=0,
				 angular_velocity=0, fuel='RP-1', oxidizer='H2O2_98%', mixture_ratio=5, g_limiter=6, isp=0):

		self.mass = mass    # Rocket's mass at launch
		self.propellant_mass_fraction = propellant_mass_fraction    # 1 - dry weight at launch / fueled weight at launch
		self.dry_mass = -(self.propellant_mass_fraction - 1) * self.mass
		self.propellant_mass = self.mass - self.dry_mass
		self.fuel_mass = self.propellant_mass / (mixture_ratio + 1)
		self.oxidizer_mass = (mixture_ratio * self.propellant_mass) / (mixture_ratio + 1)
		self.isp = isp    # Rocket engine's specific impulse | Used Rocket Propellant Analysis (RPA) software

		self.radius = altitude + Earth.radius
		self.radial_velocity = radial_velocity
		self.angular_velocity = angular_velocity + Earth.angular_velocity

		self.fuel = fuel
		self.oxidizer = oxidizer
		self.mixture_ratio = mixture_ratio

		self.g_limiter = g_limiter    # Limits the amount of g forces can experience

rocket = Rocket(1000, mixture_ratio=7.4)

print(rocket.propellant_mass)
print(rocket.oxidizer_mass)
print(rocket.fuel_mass)
print(rocket.oxidizer_mass + rocket.fuel_mass)