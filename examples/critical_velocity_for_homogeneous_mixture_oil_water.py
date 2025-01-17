
from pvtlib import fluid_mechanics

surface_tension_oil_water = 0.025 # [N/m]
oil_density = 750 # [kg/m³]
water_density = 1000 # [kg/m³]
oil_viscosity = 0.005 # [Pa.s]
pipe_diameter = 0.1 # [m]

Vc_hor = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_horizontal(
    ST_oil_aq=surface_tension_oil_water, 
    rho_o=oil_density,
    rho_aq=water_density, 
    Visc_o=oil_viscosity, 
    D=pipe_diameter
)

print(f"Critical velocity for homogeneous oil water mixture for the given conditions: {Vc_hor:.2f} m/s")


Vc_vert = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_vertical(
    beta=10.0, 
    ST_oil_aq=surface_tension_oil_water, 
    rho_o=oil_density,
    rho_aq=water_density, 
    Visc_o=oil_viscosity, 
    D=pipe_diameter
)

print(f"Critical velocity for homogeneous oil water mixture in a vertical pipe for the given conditions: {Vc_vert:.2f} m/s")