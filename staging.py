import matplotlib.pyplot as plt
import numpy as np
import math
import rocket
import planets

Earth = planets.Earth()    # Planet reference information

stage_propellant_mass_fraction = 0.80
mass_percentages = [0.75, 0.20, 0.05]    # First stage is 75% of total rocket mass, etc.
total_rocket_mass = 1000
burn_time = [100, 160, 320]
angle = [45, 80, 90]
start_time = 0
altitude = 22000
altitude_start = altitude
rad_velocity = 0
tan_velocity = 0

stage_masses = [total_rocket_mass * mass_percentage for mass_percentage in mass_percentages]   # [0] = first stage, [1] = second stage, and [2] = third stage
total_masses_by_section = [sum(stage_masses[i:3]) for i in range(0, 3)]
stage_dry_masses = [(1 - stage_propellant_mass_fraction) * stage_masses[i] for i in range(0, 3)]    # The individual's stage dry mass
stage_propellant_masses = [stage_masses[i] - stage_dry_masses[i] for i in range(0, 3)]    # The individual's stage wet mass
stage_propellant_mass_fractions = [stage_propellant_masses[i] / total_masses_by_section[i] for i in range(0, 3)]    # Propellant mass / initial mass

# Stage 1
# INCLUDE TAGENTIAL VELOCITY
print(tan_velocity)
stage = 1
stage1 = rocket.Rocket(total_masses_by_section[stage - 1],
                       burn_time[stage - 1],
                       start_time=start_time, altitude=altitude, velocity_tangential=tan_velocity, velocity_radial=0, propellant_mass_fraction=stage_propellant_mass_fractions[stage - 1], mixture_ratio=7.4, tank_pressure=7e6,
                       tank_safety_factor=1.2, angle=angle[stage - 1])
stage1.calc(burn_time[stage - 1])
altitude = stage1.log[-1][1]    # Altitude, meters
rad_velocity = stage1.log[-1][2]    # Radial velocity, m/s
tan_velocity = stage1.log[-1][8] - (Earth.velocity_angular * (Earth.radius + altitude_start))    # Tangential velocity, m/s
start_time += burn_time[stage - 1]

# Stage 2
print(tan_velocity)
stage = 2
stage2 = rocket.Rocket(total_masses_by_section[stage - 1], burn_time[stage - 1], start_time=start_time, altitude=altitude, velocity_tangential=tan_velocity, velocity_radial=rad_velocity, propellant_mass_fraction=stage_propellant_mass_fractions[stage - 1], mixture_ratio=7.4, tank_pressure=7e6,
                       tank_safety_factor=1.2, angle=angle[stage - 1])
stage2.calc(burn_time[stage - 1])
altitude = stage2.log[-1][1]    # Altitude, meters
rad_velocity = stage2.log[-1][2]    # Radial velocity, m/s
tan_velocity = stage2.log[-1][8] - (Earth.velocity_angular * (Earth.radius + altitude_start))    # Tangential velocity, m/s
start_time += burn_time[stage - 1]

# Stage 3
print(tan_velocity)
stage = 3
stage3 = rocket.Rocket(total_masses_by_section[stage - 1], burn_time[stage - 1], start_time=start_time, altitude=altitude, velocity_tangential=tan_velocity, velocity_radial=rad_velocity, propellant_mass_fraction=stage_propellant_mass_fractions[stage - 1], mixture_ratio=7.4, tank_pressure=7e6,
                       tank_safety_factor=1.2, angle=angle[stage - 1])
stage3.calc(300)


# Plots
time = [row[0] for row in stage1.log]
altitude = [row[1] / 1000 for row in stage1.log]
velocity_radial = [row[2] for row in stage1.log]
velocity_tangential = [row[8] for row in stage1.log]
velocity_total = [row[9] for row in stage1.log]
acceleration_radial = [row[3] / 9.805 for row in stage1.log]    # Unit converted from m/s2 to G's
acceleration_tangential = [row[7] / 9.805 for row in stage1.log]
acceleration_total = [row[10] / 9.805 for row in stage1.log]
thrust = [row[4] for row in stage1.log]
drag = [row[5] for row in stage1.log]
mass = [row[6] for row in stage1.log]
horizontal = [row[11] / 1000 for row in stage1.log]    # Units converted from m to km
theta = [row[12] for row in stage1.log]

f, ax = plt.subplots(2, 5)
plt.legend(loc='upper left')

ax[0, 0].scatter(time, altitude, label='First Stage')
ax[0, 0].set_title('Altitude [km]')
plt.xlabel('time [s]')

ax[0, 1].scatter(time, velocity_radial, label='First Stage')
ax[0, 1].set_title('Radial Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 2].scatter(time, velocity_tangential, label='First Stage')
ax[0, 2].set_title('Tangential Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 3].scatter(time, velocity_total, label='First Stage')
ax[0, 3].set_title('Total Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 4].scatter(time, horizontal, label='First Stage')
ax[0, 4].set_title('Horizontal arc distance traveled [km]')
plt.xlabel('time [s]')

ax[1, 0].scatter(time, acceleration_total, label='First Stage')
ax[1, 0].set_title('Acceleration [g]')
plt.xlabel('time [s]')

ax[1, 2].scatter(time, thrust, label='First Stage')
ax[1, 2].set_title('Thrust [N]')
plt.xlabel('time [s]')

ax[1, 3].scatter(time, drag, label='First Stage')
ax[1, 3].set_title('Drag [N]')
plt.xlabel('time [s]')

ax[1, 4].scatter(time, theta, label='First Stage')
ax[1, 4].set_title('Theta [deg]')
plt.xlabel('time [s]')


time = [row[0] for row in stage2.log]
altitude = [row[1] / 1000 for row in stage2.log]
velocity_radial = [row[2] for row in stage2.log]
velocity_tangential = [row[8] for row in stage2.log]
velocity_total = [row[9] for row in stage2.log]
acceleration_radial = [row[3] / 9.805 for row in stage2.log]    # Unit converted from m/s2 to G's
acceleration_tangential = [row[7] / 9.805 for row in stage2.log]
acceleration_total = [row[10] / 9.805 for row in stage2.log]
thrust = [row[4] for row in stage2.log]
drag = [row[5] for row in stage2.log]
mass = [row[6] for row in stage2.log]
horizontal = [row[11] / 1000 for row in stage2.log]    # Units converted from m to km
theta = [row[12] for row in stage2.log]


ax[0, 0].scatter(time, altitude, label='Second Stage')
ax[0, 0].set_title('Altitude [km]')
plt.xlabel('time [s]')

ax[0, 1].scatter(time, velocity_radial, label='Second Stage')
ax[0, 1].set_title('Radial Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 2].scatter(time, velocity_tangential, label='Second Stage')
ax[0, 2].set_title('Tangential Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 3].scatter(time, velocity_total, label='Second Stage')
ax[0, 3].set_title('Total Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 4].scatter(time, horizontal, label='Second Stage')
ax[0, 4].set_title('Horizontal arc distance traveled [km]')
plt.xlabel('time [s]')

ax[1, 0].scatter(time, acceleration_total, label='Second Stage')
ax[1, 0].set_title('Acceleration [g]')
plt.xlabel('time [s]')

ax[1, 2].scatter(time, thrust, label='Second Stage')
ax[1, 2].set_title('Thrust [N]')
plt.xlabel('time [s]')

ax[1, 3].scatter(time, drag, label='Second Stage')
ax[1, 3].set_title('Drag [N]')
plt.xlabel('time [s]')

ax[1, 4].scatter(time, theta, label='Second Stage')
ax[1, 4].set_title('Theta [deg]')
plt.xlabel('time [s]')


time = [row[0] for row in stage3.log]
altitude = [row[1] / 1000 for row in stage3.log]
velocity_radial = [row[2] for row in stage3.log]
velocity_tangential = [row[8] for row in stage3.log]
velocity_total = [row[9] for row in stage3.log]
acceleration_radial = [row[3] / 9.805 for row in stage3.log]    # Unit converted from m/s2 to G's
acceleration_tangential = [row[7] / 9.805 for row in stage3.log]
acceleration_total = [row[10] / 9.805 for row in stage3.log]
thrust = [row[4] for row in stage3.log]
drag = [row[5] for row in stage3.log]
mass = [row[6] for row in stage3.log]
horizontal = [row[11] / 1000 for row in stage3.log]    # Units converted from m to km
theta = [row[12] for row in stage3.log]


ax[0, 0].scatter(time, altitude, label='Third Stage')
ax[0, 0].set_title('Altitude [km]')
plt.xlabel('time [s]')

ax[0, 1].scatter(time, velocity_radial, label='Third Stage')
ax[0, 1].set_title('Radial Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 2].scatter(time, velocity_tangential, label='Third Stage')
ax[0, 2].set_title('Tangential Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 3].scatter(time, velocity_total, label='Third Stage')
ax[0, 3].set_title('Total Velocity [m/s]')
plt.xlabel('time [s]')

ax[0, 4].scatter(time, horizontal, label='Third Stage')
ax[0, 4].set_title('Horizontal arc distance traveled [km]')
plt.xlabel('time [s]')

ax[1, 0].scatter(time, acceleration_total, label='Third Stage')
ax[1, 0].set_title('Acceleration [g]')
plt.xlabel('time [s]')

ax[1, 2].scatter(time, thrust, label='Third Stage')
ax[1, 2].set_title('Thrust [N]')
plt.xlabel('time [s]')

ax[1, 3].scatter(time, drag, label='Third Stage')
ax[1, 3].set_title('Drag [N]')
plt.xlabel('time [s]')

ax[1, 4].scatter(time, theta, label='Third Stage')
ax[1, 4].set_title('Theta [deg]')
plt.xlabel('time [s]')

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
plt.show()
