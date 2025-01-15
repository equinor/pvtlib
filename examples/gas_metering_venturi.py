from pvtlib.metering import differential_pressure_flowmeters
from pvtlib import AGA8

# Define the metering device
D = 0.25 # Inlet diameter [m]
d = 0.20 # Throat diameter [m]
dP = 300.0 # Venturi differential pressure [mbar]
P = 50.0 # Pressure [bara]
T = 40.0 # Temperature [C]

composition = {
    'N2' : 1.0,
    'CO2' : 1.0,
    'C1' : 90.0,
    'C2' : 5.0,
    'C3' : 2.0,
    'iC4' : 0.5,
    'nC4' : 0.5
}

# Set up AGA8 object for GERG-2008 equation. This process runs the setup for the given equation, and is only needed once.
gerg = AGA8('GERG-2008')

# Calculate gas properties
gas_properties = gerg.calculate_from_PT(
    composition=composition,
    pressure=P,
    pressure_unit='bara',
    temperature=T,
    temperature_unit='C'
)

# Print mass density
print(f"Mass density: {gas_properties['rho']:.1f} kg/m3\n")

# Calculate beta venturi
beta = differential_pressure_flowmeters.calculate_beta_DP_meter(
    D=D,
    d=d
)

# Print venturi beta
print(f"Venturi beta: {beta:.1f}\n")

# Calculate expansibility venturi
epsilon = differential_pressure_flowmeters.calculate_expansibility_venturi(
    P1=P,
    dP=dP,
    beta=beta,
    kappa=gas_properties['kappa'] # Isentropic exponent
)

# Print venturi expansibility
print(f"Venturi expansibility: {epsilon:.4f}\n")

# Calculate venturi
results = differential_pressure_flowmeters.calculate_flow_venturi(
    D=D,
    d=d,
    dP=dP,
    rho1=gas_properties['rho'],
    epsilon=epsilon
)

# Print venturi results
print(f'Venturi massflow: {results["MassFlow"]:.1f} kg/h')
print(f'Venturi volumeflow: {results["VolFlow"]:.1f} m3/h')
print(f'Venturi velocity: {results["Velocity"]:.1f} m/s')
