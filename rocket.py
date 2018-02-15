import matplotlib.pyplot as plt
import math
import planets
import csv


class Rocket(object):
    ''' Describes a single stage rocket. Use metric units. '''

    def __init__(self, position, velocity, acceleration, engine,
                 vehicle, start=0, flight_time=120, time_step=0.0625):
        self.step = time_step    # Time increment per iteratin
        self.log = []    # Stores flight information
        self.time = start    # Rocket start time
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.vehicle = vehicle
        self.engine = engine
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
            self.log.append([self.time, self.position.altitude,
                             self.velocity.radial, self.acceleration.radial,
                             self.thrust, self.drag, self.vehicle.mass.total,
                             self.acceleration.tangential, self.velocity.tangential,
                             self.velocity.total, self.acceleration.total,
                             self.position.horizontal, self.position.theta])

    def plotter(self):
        time = [row[0] for row in self.log]
        altitude = [row[1] / 1000 for row in self.log]
        velocity_radial = [row[2] for row in self.log]
        velocity_tangential = [row[8] for row in self.log]
        velocity_total = [row[9] for row in self.log]
        horizontal = [row[11] / 1000 for row in self.log]    # Units converted from m to km
        acceleration_total = [row[10] / 9.805 for row in self.log]
        thrust = [row[4] for row in self.log]
        drag = [row[5] for row in self.log]
        theta = [row[12] for row in self.log]

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


class Vehicle(object):
    def __init__(self, mass, propellant_mass_fraction, mixture_ratio,
                 burn_time, tank_material, fuel, oxidizer, tank_safety_factor,
                 tank_pressure, drag_coefficent):
        self.mass = Mass(mass, propellant_mass_fraction, mixture_ratio)
        self.oxidizer_volume = self.mass.oxidizer / oxidizer_density[oxidizer]
        self.fuel_volume = self.mass.fuel / fuel_density[fuel]
        self.oxidizer_sphere_radius = ((3 * self.oxidizer_volume) /
                                       (4 * math.pi)) ** (1.0 / 3.0)
        self.fuel_sphere_radius = ((3 * self.fuel_volume) /
                                   (4 * math.pi)) ** (1.0 / 3.0)
        self.frontal_area_sphere = (math.pi * (self.oxidizer_sphere_radius ** 2)
                                    if self.oxidizer_sphere_radius > self.fuel_sphere_radius
                                    else (math.pi * (self.fuel_sphere_radius ** 2)))
        self.oxidizer_wall_thickness = tank_safety_factor * (tank_pressure * self.oxidizer_sphere_radius
                                                             / (2 * material[tank_material][0]))
        self.fuel_wall_thickness = tank_safety_factor * (tank_pressure * self.fuel_sphere_radius
                                                         / (2 * material[tank_material][0]))
        self.oxidizer_mass = (4 * math.pi / 3) * (self.oxidizer_sphere_radius ** 3 -
                                                  (self.oxidizer_sphere_radius -
                                                   self.oxidizer_wall_thickness) ** 3) * material[tank_material][1]
        self.fuel_mass = (4 * math.pi / 3) * (self.fuel_sphere_radius ** 3 -
                                              (self.fuel_sphere_radius -
                                               self.fuel_wall_thickness) ** 3) * material[tank_material][1]
        self.oxidizer_flow_rate = self.mass.oxidizer / burn_time    # kg/s
        self.fuel_flow_rate = self.mass.fuel / burn_time    # kg/s
        self.drag_coefficent = drag_coefficent


class Mass(object):
    def __init__(self, mass, propellant_mass_fraction, mixture_ratio):
        # Rocket's mass at launch
        self.total = mass    # !Does not incorporate tank mass!
        # Propellant mass fraction = wet mass at launch / full mass at launch
        self.propellant_fraction = propellant_mass_fraction
        self.dry = (1 - self.propellant_fraction) * self.total
        self.propellant = self.total - self.dry
        self.oxidizer = (mixture_ratio * self.propellant) / (mixture_ratio + 1)
        self.fuel = self.propellant / (mixture_ratio + 1)
        # !Assuming 2% unused fuel!
        self.residual_fuel = mass * propellant_mass_fraction * 0.02


class Position(object):
    def __init__(self, altitude=0, angle=0):
        self.altitude = altitude    # Initial height above the surface, meters
        self.horizontal = 0    # Arc distance travelled down range
        # Arc angle created between the current position
        # The center of the Earth, and the starting position
        self.theta = 0
        # Takes angle in degrees and converts it to radians
        # Zero degrees means the rocket is pointing away from the center of the Earth and
        # aligned with the radial axis
        # pi/2 radians is when the rocket is aligned with the tangential axis
        self.angle = angle * (math.pi / 180)


class Velocity(object):
    def __init__(self, velocity_radial=0, velocity_tangential=0, altitude=0):
        self.radial = velocity_radial
        # !Assume a stationary position over ground launch site if rocket is launched from a balloon!
        self.tangential = velocity_tangential + (Earth.velocity_angular * (Earth.radius + altitude))
        self.total = (self.radial ** 2 + self.tangential ** 2) ** 0.5


class Acceleration(object):
    def __init__(self, acceleration_radial=0, acceleration_tangential=0):
        self.radial = acceleration_radial
        self.tangential = acceleration_tangential
        self.total = (self.radial ** 2 + self.tangential ** 2) ** 0.5


class Air(object):
    def __init__(self):    # Outside air conditions
        self.temperature = 0    # Celsius
        self.pressure = 0    # kPa
        self.density = 0    # kg/m3


class Engine(object):
    def __init__(self, exhaust_velocity):
        self.exhaust_velocity = exhaust_velocity    # !Needs to be developed!


def update_air(self):
    # NASA atmospheric model | https://www.grc.nasa.gov/www/k-12/rocket/atmosmet.html
    if self.position.altitude >= 0 and self.position.altitude < 11000:
        # Celsius
        self.air.temperature = 15.04 - .00649 * self.positon.altitude
        # kPa
        self.air.pressure = 101.29 * ((self.air.temperature + 273.1) / 288.08) ** 5.256
    elif self.position.altitude >= 11000 and self.position.altitude < 25000:
        # Celsius
        self.air.temperature = -56.46
        # kPa
        self.air.pressure = 22.65 * math.exp(1.73 - 0.000157 * self.position.altitude)
    elif self.position.altitude >= 25000:
        # Celsius
        self.air.temperature = -131.21 + .00299 * self.position.altitude
        # kPa
        self.air.pressure = 2.488 * ((self.air.temperature + 273.1) / 216.6) ** -11.388
    else:
        self.position.altitude = -0.1
    # Air density in kg/m3
    self.air.density = self.air.pressure / (0.2869 * (self.air.temperature + 273.1))


def update_mass(self):
    # Prevents mass reduction after rocket uses all available fuel
    if self.vehicle.mass.propellant > self.vehicle.mass.residual_fuel:
        self.vehicle.mass.oxidizer -= self.vehicle.oxidizer_flow_rate * self.step
        self.vehicle.mass.fuel -= self.vehicle.fuel_flow_rate * self.step
        self.vehicle.mass.propellant = self.vehicle.mass.oxidizer + self.vehicle.mass.fuel
        self.vehicle.mass.total = self.vehicle.mass.dry + self.vehicle.mass.propellant


def calc_forces(self):
        # Calculate Earth's gravitional constant base on altitude
    self.g = 9.805 * (Earth.radius / (self.position.altitude + Earth.radius)) ** 2
    # Calculate rocket's thrust based on fuel & oxidizer consumption rate and gas exhaust velocity
    if self.vehicle.mass.propellant > self.vehicle.mass.residual_fuel:
        self.thrust = ((self.vehicle.oxidizer_flow_rate +
                        self.vehicle.fuel_flow_rate) * self.engine.exhaust_velocity)
    else:
        self.thrust = 0
    # Calculate rocket's drag based on vehicle's velocity relative to the surrounding air
    relative_velocity = self.velocity.tangential - Earth.velocity_angular * Earth.radius
    drag_velocity = (relative_velocity ** 2 + self.velocity.radial ** 2) ** 0.5
    if self.position.altitude <= 80000:
        self.drag = (0.5 * self.vehicle.drag_coefficent * self.air.density * drag_velocity**2 * self.vehicle.frontal_area_sphere)
    else:
        self.drag = 0


def calc_acceleration(self):
    # Reference plane is Earth's equator
    rocket_acceleration = (self.thrust - self.drag) / self.vehicle.mass.total
    radial_eng_acc = rocket_acceleration * math.cos(self.position.angle)
    tangential_eng_acc = rocket_acceleration * math.sin(self.position.angle)
    centripetal_acc = self.velocity.tangential ** 2 / (self.position.altitude + Earth.radius)
    # Radial acceleration from thrust - Earth's gravitational acceleration + centripetal acceleration
    self.acceleration.radial = radial_eng_acc - self.g + centripetal_acc
    self.acceleration.tangential = tangential_eng_acc
    self.acceleration.total = (self.acceleration.tangential ** 2 +
                               self.acceleration.radial ** 2) ** 0.5


def calc_velocity(self):
    # Calculates rocket's velocity base on acceleration in radial and tangential coordinates
    self.velocity.radial += self.acceleration.radial * self.step
    self.velocity.tangential += self.acceleration.tangential * self.step
    self.velocity.total = (self.velocity.radial ** 2 +
                           self.velocity.tangential ** 2) ** 0.5


def calc_position(self):
    # Height above surface
    self.position.altitude += self.velocity.radial * self.step
    # Horizontal distance from start location
    self.position.horizontal += (self.velocity.tangential -
                                 Earth.velocity_angular * (Earth.radius +
                                                           self.position.altitude)) * self.step
    # Radians !Not working!
    self.position.theta += math.atan(self.velocity.tangential * self.step) / (self.position.altitude + Earth.radius)


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
# Conservation of energy is violated
