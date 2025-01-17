import pvtlib

# Specify pressure, temperature and composition
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
gerg = pvtlib.AGA8('GERG-2008')

# Calculate gas properties (default pressure and temperature units are bara and C)
gas_properties = gerg.calculate_from_PT(
    composition=composition,
    pressure=P,
    temperature=T,
)

# Set up AGA8 object for DETAIL equation.
detail = pvtlib.AGA8('DETAIL')

# Calculate gas properties
gas_properties_detail = detail.calculate_from_PT(
    composition=composition,
    pressure=P,
    temperature=T,
)

# Print mass density from GERG-2008 and DETAIL
print(f"Mass density from GERG-2008: {gas_properties['rho']:.3f} kg/m3")
print(f"Mass density from DETAIL: {gas_properties_detail['rho']:.3f} kg/m3")

# Print speed of sound from GERG-2008 and DETAIL
print(f"Speed of sound from GERG-2008: {gas_properties['w']:.3f} m/s")
print(f"Speed of sound from DETAIL: {gas_properties_detail['w']:.3f} m/s")