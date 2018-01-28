import rocket, planets

vehicle = rocket.Rocket(31, 120, propellant_mass_fraction=0.80, mixture_ratio=7.4, tank_pressure=7e6, tank_safety_factor=1.2)

for i in range(100):
	vehicle.calc()