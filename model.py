import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rocket
import planets

# Planet reference information
Earth = planets.Earth()

# Input rocket design parameters and starting conditions
setup = rocket.Setup(altitude=22000,
                     mass=1000,
                     mass_fraction=0.80,
                     mixture_ratio=5,
                     burn_time=60,
                     tank_material='Al_6061_T6',
                     fuel='RP-1',
                     oxidizer='H2O2_98%',
                     safety_factor=2,
                     tank_pressure=0,
                     drag_coefficent=0.32,
                     angle=0)

# Single stage rocket
fire = rocket.build(setup)
# fire.calc(500)
# fire.graphs()
# plt.show()


class MultiStageSetup(object):
       def __init__(self):
              self.stage1 = stage1
              self.stage2 = stage2
              self.stage3 = stage3
              self.sub_mass_fraction = [
                  self.stage1.wet_mass / (self.stage1.mass + self.stage2.mass + self.stage3.mass),
                  self.stage2.wet_mass / (self.stage2.mass + self.stage3.mass),
                  self.stage3.wet_mass / (self.stage3.mass)]


class Stage1(object):
       def __init__(self, rocket_mass, propellant_mass_fraction,
                    mass_percentage, burn_time, angle):
              self.mass_fraction = propellant_mass_fraction[0]
              self.mass_percentage = mass_percentage[0]
              self.burn_time = burn_time[0]
              self.angle = angle[0]
              self.mass = self.mass_percentage * rocket_mass
              self.wet_mass = self.mass_fraction * self.mass
              self.dry_mass = self.mass - self.wet_mass


class Stage2(object):
       def __init__(self, rocket_mass, propellant_mass_fraction,
                    mass_percentage, burn_time, angle):
              self.mass_fraction = propellant_mass_fraction[0]
              self.mass_percentage = mass_percentage[0]
              self.burn_time = burn_time[0]
              self.angle = angle[0]
              self.mass = self.mass_percentage * rocket_mass
              self.wet_mass = self.mass_fraction * self.mass
              self.dry_mass = self.mass - self.wet_mass


class Stage3(object):
       def __init__(self, rocket_mass, propellant_mass_fraction,
                    mass_percentage, burn_time, angle):
              self.mass_fraction = propellant_mass_fraction[0]
              self.mass_percentage = mass_percentage[0]
              self.burn_time = burn_time[0]
              self.angle = angle[0]
              self.mass = self.mass_percentage * rocket_mass
              self.wet_mass = self.mass_fraction * self.mass
              self.dry_mass = self.mass - self.wet_mass


stage_parms = {
    'rocket_mass': 1000,
    'propellant_mass_fraction': [0.80, 0.80, 0.80],
    'mass_percentage': [0.75, 0.20, 0.05],
    'burn_time': [100, 160, 320],
    'angle': [45, 80, 90]
}

stage1 = Stage1(**stage_parms)
stage2 = Stage2(**stage_parms)
stage3 = Stage3(**stage_parms)

# stage = 1
# stage1 = rocket.Rocket(total_masses_by_section[stage - 1],
#                        burn_time[stage - 1],
#                        start_time=start_time, altitude=altitude, velocity_tangential=tan_velocity, velocity_radial=0, propellant_mass_fraction=stage_propellant_mass_fractions[stage - 1], mixture_ratio=7.4, tank_pressure=7e6,
#                        tank_safety_factor=1.2, angle=angle[stage - 1])
# stage1.calc(burn_time[stage - 1])
# altitude = stage1.log[-1][1]    # Altitude, meters
# rad_velocity = stage1.log[-1][2]    # Radial velocity, m/s
# tan_velocity = stage1.log[-1][8] - (Earth.velocity_angular * (Earth.radius + altitude_start))    # Tangential velocity, m/s
# start_time += burn_time[stage - 1]

# stage = 2
# stage2 = rocket.Rocket(total_masses_by_section[stage - 1], burn_time[stage - 1], start_time=start_time, altitude=altitude, velocity_tangential=tan_velocity, velocity_radial=rad_velocity, propellant_mass_fraction=stage_propellant_mass_fractions[stage - 1], mixture_ratio=7.4, tank_pressure=7e6,
#                        tank_safety_factor=1.2, angle=angle[stage - 1])
# stage2.calc(burn_time[stage - 1])
# altitude = stage2.log[-1][1]    # Altitude, meters
# rad_velocity = stage2.log[-1][2]    # Radial velocity, m/s
# tan_velocity = stage2.log[-1][8] - (Earth.velocity_angular * (Earth.radius + altitude_start))    # Tangential velocity, m/s
# start_time += burn_time[stage - 1]

# # Stage 3
# stage = 3
# stage3 = rocket.Rocket(total_masses_by_section[stage - 1], burn_time[stage - 1], start_time=start_time, altitude=altitude, velocity_tangential=tan_velocity, velocity_radial=rad_velocity, propellant_mass_fraction=stage_propellant_mass_fractions[stage - 1], mixture_ratio=7.4, tank_pressure=7e6,
#                        tank_safety_factor=1.2, angle=angle[stage - 1])
# stage3.calc(300)
