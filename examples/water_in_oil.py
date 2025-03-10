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


# EXAMPLE: Water in oil
# Oil metering station with 800 kg/m3 oil density and 1000 kg/m3 water density.
# A coriolis meter measures a mix density of 800.5 kg/m3. What is the water cut?


from pvtlib import fluid_mechanics

ContaminantVolP = fluid_mechanics.contaminant_volume_percent_from_mixed_density(
        measured_total_density=800.5,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )

print(f"Water cut is: {ContaminantVolP:.2f}%")

# What is the weight percent of water in the oil?
ContaminantWeightP = fluid_mechanics.volume_percent_to_mass_percent(
    ContaminantVolP=ContaminantVolP, 
    DominantPhase_EOS_density=800, 
    ContaminantPhase_EOS_density=1000
    )

print(f"Water weight percent is: {ContaminantWeightP:.2f}%")


# EXAMPLE: Oil density corrected for water in oil
# Coriolis in an oil metering station measures a density of 800 kg/m3. Water density is 1000 kg/m3.
# A watercut meter measures 0.3 vol% water in oil. What is the corrected oil density (without the water)?

CorrectedOilDensity = fluid_mechanics.dominant_phase_corrected_density(
    measured_total_density=800, 
    ContaminantVolP=0.3, 
    ContaminantPhase_EOS_density=1000
    )

print(f"Corrected oil density is: {CorrectedOilDensity:.2f} kg/m3")