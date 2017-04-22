import cantera as ct
import matplotlib.pyplot as plt
# Input parameters of methane and air
p = 1e5  # pressure
tin_f = 300.0  # fuel inlet temperature
tin_o = 300.0  # oxidizer inlet temperature
mdot_o = 0.82  # stechiometric oxidizer inlet kg/m^2/s
mdot_f = 0.05  # stechiometric fuel inlet kg/m^2/s
comp_o = 'O2:0.21, N2:0.78, AR:0.01'  # air composition
comp_f = 'CH4:1'  # fuel composition
# Set distance between inlets to 2 cm
width = 0.02 
# Set amount of diagnostic output (0 to 5)
loglevel = 1
# Create the gas object used to evaluate all thermodynamic, kinetic, and
# transport properties.
gas = ct.Solution('gri30.xml', 'gri30_mix')
gas.TP = gas.T, p
# Create an object representing the counterflow flame configuration,
# which consists of a fuel inlet on the left, the flow in the middle,
# and the oxidizer inlet on the right.

#Temperature of flame in function of substrats temperature
f = ct.CounterflowDiffusionFlame(gas, width=width)
# Set the state of the two inlets
f.fuel_inlet.mdot = mdot_f
f.fuel_inlet.X = comp_f
f.fuel_inlet.T = tin_f
f.oxidizer_inlet.mdot = mdot_o
f.oxidizer_inlet.X = comp_o
f.oxidizer_inlet.T = tin_o
# Set the boundary emissivities
f.set_boundary_emissivities(0.0, 0.0)
f.set_refine_criteria(ratio=4, slope=0.2, curve=0.3, prune=0.04)
# Solve the problem
f.solve(loglevel, auto=True)
f.show_solution()
f.save('ch4_diffusion_temp.xml')
# write the velocity, temperature, and mole fractions to a CSV file
f.write_csv('ch4_diffusion_temp.csv', quiet=False)
f.show_stats(0)
# Plot Temperature without radiation
figTemperatureModifiedFlame = plt.figure()
plt.plot(f.flame.grid, f.T, label=tin_o )
plt.title('Temperature of the flame with change of oxidizer temperature')
plt.ylim(0,3000)
plt.xlim(0.000, 0.020)
# Loop whih changed oxidizer temperature
while tin_o <= 400:
    tin_o=tin_o+100
    f.fuel_inlet.T = tin_f
    f.oxidizer_inlet.T = tin_o
    f.solve(loglevel=1, refine_grid=False)
    f.show_solution()
    plt.plot(f.flame.grid, f.T, label=tin_o)
    plt.legend()
    plt.legend(loc=1)
plt.savefig('./ch4_diffusion_temperature.pdf')

#Temperature of flame in function of equivalence ratio
tin_f=300
tin_o=300
mdot_f = 0.025
mdot_o = 0.87-mdot_f
f = ct.CounterflowDiffusionFlame(gas, width=width)
# Set the state of the two inlets
f.fuel_inlet.mdot = mdot_f
f.fuel_inlet.X = comp_f
f.fuel_inlet.T = tin_f
f.oxidizer_inlet.mdot = mdot_o
f.oxidizer_inlet.X = comp_o
f.oxidizer_inlet.T = tin_o
# Set the boundary emissivities
f.set_boundary_emissivities(0.0, 0.0)
f.set_refine_criteria(ratio=4, slope=0.2, curve=0.3, prune=0.04)
# Solve the problem
f.solve(loglevel, auto=True)
f.show_solution()
f.save('ch4_diffusion_eq.xml')
# write the velocity, temperature, and mole fractions to a CSV file
f.write_csv('ch4_diffusion_eq.csv', quiet=False)
f.show_stats(0)
# Plot Temperature without radiation
figTemperatureModifiedFlame = plt.figure()
plt.plot(f.flame.grid, f.T, label=mdot_f/(mdot_o*0.058275) )
plt.title('Temperature of the flame with change of equivalence ratio')
plt.ylim(0,3000)
plt.xlim(0.000, 0.020)
# Loop whih changed equivalence ratio
while mdot_f <= 0.065:
    mdot_f=mdot_f+0.01
    mdot_o = 0.87-mdot_f
    f.fuel_inlet.mdot = mdot_f
    f.oxidizer_inlet.mdot = mdot_o
    f.solve(loglevel=1, refine_grid=False)
    f.show_solution()
    plt.plot(f.flame.grid, f.T, label=mdot_f/(mdot_o*0.058275))
    plt.legend()
    plt.legend(loc=1)
plt.savefig('./ch4_diffusion_eq.pdf')

#Temperature of flame in function of pressure
mdot_o = 0.82
mdot_f = 0.05
f = ct.CounterflowDiffusionFlame(gas, width=width)
# Set the state of the two inlets
f.fuel_inlet.mdot = mdot_f
f.fuel_inlet.X = comp_f
f.fuel_inlet.T = tin_f
f.oxidizer_inlet.mdot = mdot_o
f.oxidizer_inlet.X = comp_o
f.oxidizer_inlet.T = tin_o
# Set the boundary emissivities
f.set_boundary_emissivities(0.0, 0.0)
f.set_refine_criteria(ratio=4, slope=0.2, curve=0.3, prune=0.04)
# Solve the problem
f.solve(loglevel, auto=True)
f.show_solution()
f.save('ch4_diffusion_press.xml')
# write the velocity, temperature, and mole fractions to a CSV file
f.write_csv('ch4_diffusion_press.csv', quiet=False)
f.show_stats(0)
# Plot Temperature without radiation
figTemperatureModifiedFlame = plt.figure()
plt.plot(f.flame.grid, f.T, label=p )
plt.title('Temperature of the flame with change of pressure')
plt.ylim(0,3000)
plt.xlim(0.000, 0.020)
# Loop whih changed pressure
while p <= 3e5:
    p=p+2e5
    gas.TP = gas.T, p
    f = ct.CounterflowDiffusionFlame(gas, width=width)
    f.fuel_inlet.mdot = mdot_f
    f.fuel_inlet.X = comp_f
    f.fuel_inlet.T = tin_f
    f.oxidizer_inlet.mdot = mdot_o
    f.oxidizer_inlet.X = comp_o
    f.oxidizer_inlet.T = tin_o
    f.set_boundary_emissivities(0.0, 0.0)
    f.set_refine_criteria(ratio=4, slope=0.2, curve=0.3, prune=0.04)
    f.solve(loglevel, auto=True)
    f.show_solution()
    plt.plot(f.flame.grid, f.T, label=p)
    plt.legend()
    plt.legend(loc=1)
plt.savefig('./ch4_diffusion_pres.pdf')