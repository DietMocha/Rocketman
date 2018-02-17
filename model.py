import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rocket
import planets

# Planet reference information
Earth = planets.Earth()

columns = ['time', 'altitude', 'horizontal', 'rad_vel',
           'tan_vel', 'total_vel', 'rad_acc', 'tan_acc',
           'tot_acc', 'cent_acc', 'mass', 'thrust',
           'drag', 'theta']

scores = []

# Input rocket design parameters and starting conditions
for a in range(70, 85):
    for b in range(25, 10, -1):
        try:
            stage_parms = {
                'rocket_mass': 1000,
                # [stage 1, stage 2, stage 3]
                'propellant_mass_fraction': [0.80, 0.80, 0.80],
                'mass_percentage': [a / 100, b / 100, 0.05],
                'burn_time': [60, 80, 350],
                'angle': [50, 70, 70],
            }

            staging_delay = 0
            added_time = 0

            stage1 = rocket.Stage(1, **stage_parms)
            stage2 = rocket.Stage(2, **stage_parms)
            stage3 = rocket.Stage(3, **stage_parms)
            multi_stage = rocket.MultiStage(stage1, stage2, stage3)

            # Establishes overall rocket
            setup = rocket.Setup(altitude=22000,
                                 mass=100,
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

            # Modifies setup for the first stage
            setup = rocket.Setup(altitude=setup.position['altitude'],
                                 mass=stage1.mass + stage2.mass + stage3.mass,
                                 mass_fraction=multi_stage.sub_mass_fraction[stage1.stage - 1],
                                 mixture_ratio=setup.vehicle['mixture_ratio'],
                                 burn_time=stage1.burn_time,
                                 tank_material=setup.vehicle['tank_material'],
                                 fuel=setup.vehicle['fuel'],
                                 oxidizer=setup.vehicle['oxidizer'],
                                 safety_factor=setup.vehicle['tank_safety_factor'],
                                 tank_pressure=setup.vehicle['tank_pressure'],
                                 drag_coefficent=setup.vehicle['drag_coefficent'],
                                 angle=stage1.angle)
            stage = rocket.build(setup, start_time=0)
            stage.calc(stage1.burn_time)
            log = pd.DataFrame(stage.log, columns=columns)

            # Modifies setup for the second stage
            setup = rocket.Setup(altitude=log.altitude.iloc[-1],
                                 horizontal=log.horizontal.iloc[-1],
                                 velocity_radial=log.rad_vel.iloc[-1],
                                 velocity_tangential=log.tan_vel.iloc[-1] - (Earth.velocity_angular * (Earth.radius + log.altitude.iloc[-1])),
                                 mass=stage2.mass + stage3.mass,
                                 mass_fraction=multi_stage.sub_mass_fraction[stage2.stage - 1],
                                 mixture_ratio=setup.vehicle['mixture_ratio'],
                                 burn_time=stage2.burn_time,
                                 tank_material=setup.vehicle['tank_material'],
                                 fuel=setup.vehicle['fuel'],
                                 oxidizer=setup.vehicle['oxidizer'],
                                 safety_factor=setup.vehicle['tank_safety_factor'],
                                 tank_pressure=setup.vehicle['tank_pressure'],
                                 drag_coefficent=setup.vehicle['drag_coefficent'],
                                 angle=stage2.angle)
            stage = rocket.build(setup, start_time=stage1.burn_time + staging_delay)
            stage.calc(stage2.burn_time + staging_delay)
            log = pd.concat([log, pd.DataFrame(stage.log, columns=columns)], ignore_index=True)

            # Modifies setup for the thrid stage
            setup = rocket.Setup(altitude=log.altitude.iloc[-1],
                                 horizontal=log.horizontal.iloc[-1],
                                 velocity_radial=log.rad_vel.iloc[-1],
                                 velocity_tangential=log.tan_vel.iloc[-1] - (Earth.velocity_angular * (Earth.radius + log.altitude.iloc[-1])),
                                 mass=stage3.mass,
                                 mass_fraction=multi_stage.sub_mass_fraction[stage3.stage - 1],
                                 mixture_ratio=setup.vehicle['mixture_ratio'],
                                 burn_time=stage3.burn_time,
                                 tank_material=setup.vehicle['tank_material'],
                                 fuel=setup.vehicle['fuel'],
                                 oxidizer=setup.vehicle['oxidizer'],
                                 safety_factor=setup.vehicle['tank_safety_factor'],
                                 tank_pressure=setup.vehicle['tank_pressure'],
                                 drag_coefficent=setup.vehicle['drag_coefficent'],
                                 angle=stage3.angle)
            stage = rocket.build(setup, start_time=stage2.burn_time + stage1.burn_time + 2 * staging_delay)
            stage.calc(stage3.burn_time + staging_delay + added_time)
            log = pd.concat([log, pd.DataFrame(stage.log, columns=columns)], ignore_index=True)
            # gh + 0.5v^2
            specific_energy = 9.805 * (Earth.radius + log.altitude.iloc[-1]) + 0.5 * log.total_vel.iloc[-1]**2
            print(round(specific_energy / 1000000, 3), stage_parms.values())
            scores.append(round(specific_energy / 1000000, 3))
        except:
            pass
print(sorted(scores, reverse=True))
# rocket.graph(log)
