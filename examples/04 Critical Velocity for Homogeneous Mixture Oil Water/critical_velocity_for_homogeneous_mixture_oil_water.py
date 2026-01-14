"""MIT License

Copyright (c) 2025 Christian Hågenvik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


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