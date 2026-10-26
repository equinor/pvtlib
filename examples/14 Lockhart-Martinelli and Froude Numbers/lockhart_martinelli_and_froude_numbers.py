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

# Example: Lockhart-Martinelli parameter as a function of gas volume fraction and
# density ratio, and Froude numbers as a function of velocity and volume flow.
# All input values are illustrative. The plots are saved as PNG files next to this script.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from pvtlib import fluid_mechanics

output_folder = Path(__file__).parent

# Inner diameters of schedule 80 pipes, from outside diameter and wall thickness
# as tabulated in https://en.wikipedia.org/wiki/Nominal_Pipe_Size
INCH = 0.0254  # [m]
pipes = {
    '4"': (4.500 - 2 * 0.337) * INCH,   # Inner diameter [m]
    '6"': (6.625 - 2 * 0.432) * INCH,   # Inner diameter [m]
    '8"': (8.625 - 2 * 0.500) * INCH,   # Inner diameter [m]
    '12"': (12.75 - 2 * 0.687) * INCH,  # Inner diameter [m]
}


#%% Lockhart-Martinelli parameter as a function of GVF and density ratio

# X depends only on GVF and the gas-to-liquid density ratio. Gas densities of
# 10-150 kg/m3 and liquid densities of 600-1000 kg/m3 give density ratios from
# 10/1000 = 0.01 to 150/600 = 0.25.
rho_l = 1000.0  # Liquid density [kg/m3]. Any value gives the same X for a given density ratio.
GVF_values = np.linspace(0.95, 1.0, 51)  # Gas volume fraction [-]
DR_values = np.linspace(10 / 1000, 150 / 600, 49)  # Gas-to-liquid density ratio [-]

GVF_grid, DR_grid = np.meshgrid(GVF_values, DR_values, indexing='ij')
X_grid = np.zeros_like(GVF_grid)

for i, j in np.ndindex(GVF_grid.shape):
    X_grid[i, j] = fluid_mechanics.GVF_to_lockhart_martinelli(
        GVF=GVF_grid[i, j],
        density_liquid=rho_l,
        density_gas=DR_grid[i, j] * rho_l,  # Gas density giving the chosen density ratio [kg/m3]
    )

fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(GVF_grid * 100, DR_grid, X_grid, cmap='jet', rstride=2, cstride=2,
                linewidth=0.3, edgecolors='k', alpha=0.9)
ax.set_xlabel('GVF [%]', labelpad=12)
ax.set_ylabel(r'Density ratio $\rho_g/\rho_l$ [-]', labelpad=12)
ax.zaxis.set_rotate_label(False)
ax.set_zlabel('$X_{LM}$ [-]', labelpad=8, rotation=90)
ax.view_init(elev=25, azim=60)
ax.set_title('Lockhart-Martinelli parameter vs GVF and density ratio')
fig.savefig(output_folder / 'lockhart_martinelli_surface.png', dpi=150, bbox_inches='tight')
plt.close(fig)


#%% Froude number as a function of velocity, for different pipe sizes

velocities = np.linspace(0.0, 30.0, 301)  # Velocity [m/s]

fig, ax = plt.subplots(figsize=(9, 6))
for pipe_size, D in pipes.items():
    Fr = [fluid_mechanics.froude_number(v=v, D=D) for v in velocities]
    ax.plot(velocities, Fr, label=f'{pipe_size} sch. 80, D = {D * 1000:.1f} mm')

ax.set_xlabel('Velocity [m/s]')
ax.set_ylabel('Froude number $v/\\sqrt{gD}$ [-]')
ax.set_title('Froude number vs velocity')
ax.grid()
ax.legend()
fig.savefig(output_folder / 'froude_number_vs_velocity.png', dpi=150, bbox_inches='tight')
plt.close(fig)


#%% Gas densimetric Froude number as a function of gas volume flow, 6" pipe

D = pipes['6"']  # Inner pipe diameter [m]
rho_l = 800.0  # Liquid density [kg/m3]
gas_densities = [10.0, 50.0, 100.0, 150.0]  # Gas density [kg/m3]
VolFlow_gas_values = np.linspace(0.0, 2000.0, 201)  # Gas volume flow at line conditions [m3/h]

fig, ax = plt.subplots(figsize=(9, 6))
for rho_g in gas_densities:
    Fr_gas = []
    for VolFlow_gas in VolFlow_gas_values:
        # Superficial gas velocity [m/s] from the gas volume flow [m3/h]
        v_sg = fluid_mechanics.superficial_velocity(Q_phase=VolFlow_gas, D=D)
        Fr_gas.append(fluid_mechanics.densimetric_froude_number(
            v=v_sg, D=D, rho_phase=rho_g, rho_other=rho_l))
    ax.plot(VolFlow_gas_values, Fr_gas, label=f'$\\rho_g$ = {rho_g:.0f} kg/m³')

ax.set_xlabel('Gas volume flow at line conditions [m³/h]')
ax.set_ylabel('Gas densimetric Froude number $Fr_g$ [-]')
ax.set_title(f'Gas densimetric Froude number, 6" sch. 80 (D = {D * 1000:.1f} mm), '
             f'$\\rho_l$ = {rho_l:.0f} kg/m³')
ax.grid()
ax.legend()
fig.savefig(output_folder / 'densimetric_froude_number_vs_volume_flow.png', dpi=150, bbox_inches='tight')
plt.close(fig)

print(f'Plots saved in {output_folder}')
