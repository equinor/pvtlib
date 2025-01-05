import numpy as np

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