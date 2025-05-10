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



# This example demonstrates how to use the `interpolate` function to retrieve the corresponding calibration error for a given flowrate, for a given calibration curve.

from pvtlib.utilities import linear_interpolation
import matplotlib.pyplot as plt

# Calibration data. NB: X-values (typically Reynolds number or flowrate, must be sorted by increasing value)
volume_flowrate = [100, 300, 900, 1400, 1900, 2500, 3100] # m3/h
# The order of the calibration errors must correspond to the volme flowrates given
calibration_error = [-0.09, -0.05, 0.1, 0.15, 0.16, 0.14, 0.05] # % of reading

# Indicated volume flowrate
Q_ind = 2791 #m3/h

error = linear_interpolation(Q_ind, volume_flowrate, calibration_error)

# Plot the calibration curve
plt.figure(figsize=(8, 6))
plt.plot(volume_flowrate, calibration_error, marker='o', linestyle='-', color='b', label='Calibration Curve')

plt.plot(Q_ind, error, marker='X', color='r', markersize=10, label='Interpolated point')

plt.title('Calibration Curve')
plt.xlabel('Volume Flowrate (m³/h)')
plt.ylabel('Calibration Error (% of reading)')
plt.grid(True)
plt.legend()
plt.show()

print(f"At {Q_ind} m³/h flowrate, the interpolated calibration error is {error:.2f} %")




