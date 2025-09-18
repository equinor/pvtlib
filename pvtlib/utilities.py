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

import numpy as np

def linear_interpolation(x, x_values, y_values):
    '''
    Perform linear interpolation to estimate the value of a dependent variable y for a given independent variable x, based on a set of given x and y values.

    If x is below lowest value in x_values the function returns the lowest value in y_values
    If x is above the highest value in x_values the function returns the highest value in y_values
    The calibration arrays must be sorted from lowest to highest x values (flow/Reynolds)

    This function can for example be used for a calibration curve, where x could be the flow or Reynolds number and y could be the corresponding calibration error or discharge coefficient. 
    
    Parameters:
    -----------
    x : float
        The independent variable value for which the dependent variable needs to be estimated.
    x_values : list
        A list of float values representing the x values of the data set used for interpolation.
    y_values : list
        A list of float values representing the y values of the data set used for interpolation.
        
    Returns:
    --------
    y : float
        The estimated value of the dependent variable y for the given independent variable x.
    '''
    
    # Check if input values are valid
    if np.isnan(x):
        return np.nan
    # Check if x_values and y_values have the same length
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length.")
    # Check if x_values is sorted in ascending order
    if any(x_values[i] > x_values[i + 1] for i in range(len(x_values) - 1)):
        raise ValueError("x_values must be sorted in ascending order.")

    if x < x_values[0]:
        y = y_values[0]
    elif x > x_values[-1]:
        y =  y_values[-1]
    else:
        for i in range(len(x_values) - 1):
            if x_values[i] <= x <= x_values[i + 1]:
                x1, x2 = x_values[i], x_values[i + 1]
                y1, y2 = y_values[i], y_values[i + 1]
                m = (y2 - y1) / (x2 - x1)
                y = m * (x - x1) + y1
            
    return y


#%% Deviation calculations (Equations for calculating relative deviation between two properties)
def relative_difference(prop_A, prop_B):
    '''
    
    Parameters
    ----------
    prop_A : float
        property A
    prop_B : float
        Property B

    Returns
    -------
    diff : float
        Relative difference between prop_A and prop_B [%]

    '''
    if prop_A+prop_B == 0: #prevent divide by 0 error
        diff = np.nan
    else:
        diff=100*(prop_A-prop_B)/((prop_A+prop_B)/2)
    
    return diff



def calculate_deviation(observed_value, reference_value):
    '''
    Calculates the difference between the observed value and the reference value   

    Parameters
    ----------
    observed_value : float
        Measurement by test object
    reference_value : float
        Reference measurement

    Returns
    -------
    float
        Difference between observed and reference value

    '''
    
    return observed_value - reference_value


def calculate_relative_deviation(observed_value, reference_value):
    '''
    Calculates the error percentage as the percentage difference between the observed value and the reference value    

    Parameters
    ----------
    observed_value : float
        Measurement by test object
    reference_value : float
        Reference measurement

    Returns
    -------
    float
        Error percentage between observed and measured value

    '''
    
    if reference_value == 0:
        return np.nan
    else:
        return 100 * (observed_value - reference_value) / reference_value


def calculate_max_min_diffperc(array):
    '''
    Calculate the percentage deviation between the max and min value of an array, relative to the mean of the array

    Parameters
    ----------
    array : list
        list, numpy array or similar object.

    Returns
    -------
    max_min_diff : float
        Difference percentage between max and min value of array relative to the mean of the array.
    '''
    
    if np.max(array) == 0:
        max_min_diff=np.nan
    else:
        max_min_diff=100*(np.max(array)-np.min(array))/np.mean(array)
        
    return max_min_diff