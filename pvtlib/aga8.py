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

The code is based upon the python library pyaga8, which is again based upon the open source rust package aga8 (https://crates.io/crates/aga8)
"""

import numpy as np
import pyaga8
from scipy import optimize

class AGA8:
    """
    A class to perform gas property calculations using the AGA8 equations of state, DETAIL [1]_ and GERG-2008 [2]_.
    equation : str, optional
        The equation of state to use. Must be either 'GERG-2008' or 'DETAIL'. Default is 'GERG-2008'.
    Attributes
    equation : str
        The equation of state being used.
    adapter : object
        The adapter object corresponding to the selected equation of state.
    Methods
    calculate_from_PT(composition, pressure, temperature, pressure_unit='bara', temperature_unit='C', molar_mass=None)
        Calculate gas properties using pressure, temperature, and composition as input.
    calculate_from_rhoT(composition, mass_density, temperature, temperature_unit='C', molar_mass=None)
        Calculate gas properties using mass density, temperature, and composition as input.
    
    References
    ----------
    .. [1] AGA Report No. 8 Part 1 Third Edition, Thermodynamic Properties of Natural Gas and Related Gases - DETAIL and GROSS Equations of State, 2017
    .. [2] AGA Report No. 8 Part 2 First Edition, Thermodynamic Properties of Natural Gas and Related Gases - Gerg-2008 Equation of State, 2017
    """ 

    def __init__(self, equation = 'GERG-2008'):

        self.equation = equation.upper()

        if self.equation not in ['GERG-2008', 'DETAIL']:
            raise Exception('Invalid equation selected. Must be either GERG-2008 or DETAIL')
        
        if self.equation == 'GERG-2008':
            self.adapter = pyaga8.Gerg2008()

        elif self.equation == 'DETAIL':
            self.adapter = pyaga8.Detail()
        
        # Initialize molecular weights for AGA8 components
        # These are stored to ensure consistency with the equation of state being used
        self._initialize_molecular_weights()

    def _get_properties(self):
        properties = {}
        for attr in dir(self.adapter):
            if not callable(getattr(self.adapter, attr)) and not attr.startswith("__"):
                properties[attr] = getattr(self.adapter, attr)
        
        properties['pressure_bara'] = properties['pressure']/100
        properties['temperature_C'] = properties['temperature'] - 273.15

        return properties

    def _initialize_molecular_weights(self):
        """
        Initialize molecular weights for all AGA8 components.
        These values are from official AGA8 standards and differ between GERG-2008 and DETAIL equations.
        """
        # Component list in consistent order
        self.aga8_components = ['C1', 'N2', 'CO2', 'C2', 'C3', 'iC4', 'nC4', 'iC5', 'nC5', 
                                'nC6', 'nC7', 'nC8', 'nC9', 'nC10', 'H2', 'O2', 'CO', 
                                'H2O', 'H2S', 'He', 'Ar']
        
        # Molecular weights from official AGA8 NIST github repo [g/mol]
        if self.equation == 'GERG-2008':
            self.molecular_weights = np.array([
                16.04246,   # C1 - methane
                28.0134,    # N2 - nitrogen
                44.0095,    # CO2 - carbon dioxide
                30.06904,   # C2 - ethane
                44.09562,   # C3 - propane
                58.1222,    # iC4 - isobutane
                58.1222,    # nC4 - n-butane
                72.14878,   # iC5 - isopentane
                72.14878,   # nC5 - n-pentane
                86.17536,   # nC6 - hexane
                100.20194,  # nC7 - heptane
                114.22852,  # nC8 - octane
                128.2551,   # nC9 - nonane
                142.28168,  # nC10 - decane
                2.01588,    # H2 - hydrogen
                31.9988,    # O2 - oxygen
                28.0101,    # CO - carbon monoxide
                18.01528,   # H2O - water
                34.08088,   # H2S - hydrogen sulfide
                4.002602,   # He - helium
                39.948      # Ar - argon
            ], dtype=np.float64)
        elif self.equation == 'DETAIL':
            self.molecular_weights = np.array([
                16.043,     # C1 - methane
                28.0135,    # N2 - nitrogen
                44.01,      # CO2 - carbon dioxide
                30.07,      # C2 - ethane
                44.097,     # C3 - propane
                58.123,     # iC4 - isobutane
                58.123,     # nC4 - n-butane
                72.15,      # iC5 - isopentane
                72.15,      # nC5 - n-pentane
                86.177,     # nC6 - hexane
                100.204,    # nC7 - heptane
                114.231,    # nC8 - octane
                128.258,    # nC9 - nonane
                142.285,    # nC10 - decane
                2.0159,     # H2 - hydrogen
                31.9988,    # O2 - oxygen
                28.01,      # CO - carbon monoxide
                18.0153,    # H2O - water
                34.082,     # H2S - hydrogen sulfide
                4.0026,     # He - helium
                39.948      # Ar - argon
            ], dtype=np.float64)
        
        # Create component index mapping for fast lookup
        self.component_indices = {comp: idx for idx, comp in enumerate(self.aga8_components)}
    
    def _calculate_density(self):
        if self.equation == 'GERG-2008':
            self.adapter.calc_density(0)
        elif self.equation == 'DETAIL':
            self.adapter.calc_density()

    def calculate_from_PT(self, composition: dict, pressure: float, temperature: float, pressure_unit = 'bara', temperature_unit = 'C', molar_mass = None):
        """
        Calculate gas properties using AGA8 with pressure, temperature and composition as input.

        Parameters
        ----------
        composition : dict
            Composition containing component name as key and mole percent or mole fraction as value.
            
            C1 : methane
            N2 : nitrogen
            CO2 : carbon_dioxide
            C2 : ethane
            C3 : propane
            iC4 : isobutane
            nC4 : n_butane
            iC5 : isopentane
            nC5 : n_pentane
            nC6 : hexane
            nC7 : heptane
            nC8 : octane
            nC9 : nonane
            nC10 : decane
            H2 : hydrogen
            O2 : oxygen
            CO : carbon_monoxide
            H2O : water
            H2S : hydrogen_sulfide
            He : helium
            Ar : argon
            
        pressure : float
            P - Pressure

        temperature : float
            T - Temperature

        pressure_unit : str
            Unit of pressure. The default unit is bara.

        temperature_unit : str
            Unit of temperature. The default unit is Celsius (C).

        molar_mass : float, optional
            Molar mass can be given as an optional input [kg/kmol]. If this is given, this molar mass will be used to calculate the mass density instead of the AGA8 calculated molar mass. 
            The default is None. In that case the AGA8 calculated molar mass will be used.

        Returns
        -------
        results : TYPE
            Dictionary with properties from AGA8.
            
            '     P - Pressure [kPa]
            '     T - Temperature [k]
            '     Z - Compressibility factor [-]
            '  dPdD - First derivative of pressure with respect to density at constant temperature [kPa/(mol/l)]
            'd2PdD2 - Second derivative of pressure with respect to density at constant temperature [kPa/(mol/l)^2]
            'd2PdTD - Second derivative of pressure with respect to temperature and density [kPa/(mol/l)/K]
            '  dPdT - First derivative of pressure with respect to temperature at constant density (kPa/K)
            '     U - Internal energy [J/mol]
            '     H - Enthalpy [J/mol]
            '     S - Entropy [J/(mol-K)]
            '    Cv - Isochoric heat capacity [J/(mol-K)]
            '    Cp - Isobaric heat capacity [J/(mol-K)]
            '     W - Speed of sound [m/s]
            '     G - Gibbs energy [J/mol]
            '    JT - Joule-Thomson coefficient [K/kPa]
            ' Kappa - Isentropic Exponent [-]
            '     A - Helmholtz energy [J/mol]
            '     D - Molar density [mol/l]
            '    mm - Molar mass [g/mol]
            '   rho - Mass density [kg/m3]
            
            '   gas_composition - Dictionary containing the composition used in the calculations

        """

        #Convert pressure to kPa
        pressure_kPa = _pressure_unit_conversion(
            pressure_value=pressure,
            pressure_unit=pressure_unit
            )

        #Convert temperature to K
        temperature_K = _temperature_unit_conversion(
            temperature_value=temperature,
            temperature_unit=temperature_unit
            )

        results = {}

        #Convert composition to aga8 format
        Aga8fluid, Aga8fluidDict = to_aga8_composition(composition)
        
        # Check if any input is nan, including composition values. In case any values are nan, return a dictionary with all properties as nan
        if (
            np.isnan(pressure_kPa)
            or np.isnan(temperature_K)
            or any(np.isnan(v) for v in composition.values())
        ):
                    # get properties
            results = {key: np.nan for key in self._get_properties().keys()}
        else:

            self.adapter.set_composition(Aga8fluid)
            self.adapter.pressure = pressure_kPa
            self.adapter.temperature = float(temperature_K)

            self._calculate_density()
            self.adapter.calc_properties()  # calculate properties

            # get properties
            results = self._get_properties()


        #Calculate mass density
        if molar_mass is None:
            results['rho'] = results['d']*results['mm'] #mol/l * g/mol = g/l = kg/m3
        else:
            results['rho'] = results['d']*molar_mass #mol/l * g/mol = g/l = kg/m3

        #Add gas composition to results
        results['gas_composition'] = Aga8fluidDict

        return results
    

    
    def calculate_from_rhoT(self, composition: dict, mass_density: float, temperature: float, temperature_unit = 'C', molar_mass = None):
        '''
        Calculate gas properties using AGA8 with mass density, temperature and composition as input.
        
        Parameters
        ----------
        gas_composition : dict
            Dictionary with component name as key and mole percent or mole fraction as value.
        mass_density : float
            Mass density [kg/m3]
        temperature : float
            Temperature. Unit of measure is defined by temperature_unit.
        temperature_unit : TYPE, optional
            Unit of measure for temperature. The default is 'C'.
        molar_mass : float, optional
            Molar mass can be given as an optional input [kg/kmol]. If this is given, this molar mass will be used to calculate the mass density instead of the AGA8 calculated molar mass. The default is None. In that case the AGA8 calculated molar mass will be used. 
        
        Returns
        -------
        results : dict
            Dictionary with properties from AGA8 (same as for the calculatcalculate_from_PT method)
        '''
        #Convert temperature to K
        temperature_K = _temperature_unit_conversion(
            temperature_value=temperature,
            temperature_unit=temperature_unit
            )

        results = {}

        #Convert composition to aga8 format
        Aga8fluid, Aga8fluidDict = to_aga8_composition(composition)

        # Check if any input is nan, including composition values and mass_density
        if (
            np.isnan(mass_density)
            or np.isnan(temperature_K)
            or any(np.isnan(v) for v in composition.values())
        ):
            # get properties
            results = {key: np.nan for key in self._get_properties().keys()}
            # Add gas composition to results
            results['gas_composition'] = Aga8fluidDict
            return results

        self.adapter.set_composition(Aga8fluid)
        
        #Calculate molar mass if the molar mass is not specified
        if molar_mass is None:
            self.adapter.calc_molar_mass()
            molar_mass = self.adapter.mm
        
        #Calculate molar density (mol/l)
        if molar_mass !=0:
            molar_density = mass_density / molar_mass #kg/m3 / kg/kmol --> kmol/m3 --> mol/l
        else:
            #Return blank dictionary of molar mass is 0, to avoid division by zero error
            return {}
        
        self.adapter.d = molar_density
        self.adapter.temperature = temperature_K

        pressure_kPa = self.adapter.calc_pressure()
        
        #Set the pressure obtained from the calculation
        self.adapter.pressure = pressure_kPa
        
        self.adapter.calc_properties()  # calculate properties

        results = self._get_properties()  # get properties

        #Calculate mass density
        if molar_mass is None:
            results['rho'] = results['d']*results['mm'] #mol/l * g/mol = g/l = kg/m3
        else:
            results['rho'] = results['d']*molar_mass #mol/l * g/mol = g/l = kg/m3

        #Add gas composition to results
        results['gas_composition'] = Aga8fluidDict

        return results
    
    
    def calculate_from_PH(self, composition: dict, pressure: float, enthalpy: float, pressure_unit = 'bara', molar_mass = None):
        """
        Calculate gas properties using AGA8 with pressure, enthalpy and composition as input.

        Parameters
        ----------
        composition : dict
            The composition of the gas mixture as a dictionary where keys are component names and values are their mole fractions.
        pressure : float
            Pressure. Unit is defined by pressure_unit.
        enthalpy : float
            Enthalpy, H [J/mol]
        pressure_unit : str, optional
            The unit of the pressure, by default 'bara'.
        molar_mass : float, optional
            The molar mass of the gas mixture, by default None. If None, the AGA8 molar mass is used. 
        Returns
        -------
        results : dict
            Dictionary with properties from AGA8 (same as for the calculatcalculate_from_PT method)
        """

        temperature_unit = 'C'

        # Check if any input is nan, including composition values, pressure, or enthalpy
        pressure_kPa = _pressure_unit_conversion(
            pressure_value=pressure,
            pressure_unit=pressure_unit
        )
        if (
            np.isnan(pressure_kPa)
            or np.isnan(enthalpy)
            or any(np.isnan(v) for v in composition.values())
        ):
            # get properties
            Aga8fluid, Aga8fluidDict = to_aga8_composition(composition)
            results = {key: np.nan for key in self._get_properties().keys()}
            results['gas_composition'] = Aga8fluidDict
            return results

        def residual(temperature):
            # Extract scalar from numpy array for compatibility with numpy 2.x
            temp_scalar = temperature[0] if hasattr(temperature, '__len__') else temperature
            results = self.calculate_from_PT(composition, pressure, temp_scalar, pressure_unit, temperature_unit, molar_mass)
            return results['h'] - enthalpy
        
        temperature_guess = 20.0 # Celsius

        temperature_solution = optimize.fsolve(residual, x0=[temperature_guess])
        temperature_scalar = temperature_solution.item() if hasattr(temperature_solution, 'item') else float(temperature_solution[0])
        results = self.calculate_from_PT(composition, pressure, temperature_scalar, pressure_unit, temperature_unit, molar_mass)
        return results
    

    def calculate_from_PS(self, composition: dict, pressure: float, entropy: float, pressure_unit = 'bara', molar_mass = None):
        """
        Calculate gas properties using AGA8 with pressure, entropy and composition as input.

        Parameters
        ----------
        composition : dict
            The composition of the gas mixture as a dictionary where keys are component names and values are their mole fractions.
        pressure : float
            Pressure. Unit is defined by pressure_unit.
        entropy : float
            Entropy, S [J/mol-K]
        pressure_unit : str, optional
            The unit of the pressure, by default 'bara'.
        molar_mass : float, optional
            The molar mass of the gas mixture, by default None. If None, the AGA8 molar mass is used. 
        Returns
        -------
        results : dict
            Dictionary with properties from AGA8 (same as for the calculatcalculate_from_PT method)
        """

        temperature_unit = 'C'

        # Check if any input is nan, including composition values, pressure, or entropy
        pressure_kPa = _pressure_unit_conversion(
            pressure_value=pressure,
            pressure_unit=pressure_unit
        )
        if (
            np.isnan(pressure_kPa)
            or np.isnan(entropy)
            or any(np.isnan(v) for v in composition.values())
        ):
            # get properties
            Aga8fluid, Aga8fluidDict = to_aga8_composition(composition)
            results = {key: np.nan for key in self._get_properties().keys()}
            results['gas_composition'] = Aga8fluidDict
            return results

        def residual(temperature):
            # Extract scalar from numpy array for compatibility with numpy 2.x
            temp_scalar = temperature[0] if hasattr(temperature, '__len__') else temperature
            results = self.calculate_from_PT(composition, pressure, temp_scalar, pressure_unit, temperature_unit, molar_mass)
            return results['s'] - entropy
        
        temperature_guess = 20.0

        temperature_solution = optimize.fsolve(residual, x0=[temperature_guess])
        temperature_scalar = temperature_solution.item() if hasattr(temperature_solution, 'item') else float(temperature_solution[0])
        results = self.calculate_from_PT(composition, pressure, temperature_scalar, pressure_unit, temperature_unit, molar_mass)
        return results

    def mix(self, compositions: list, mix_weights: list, check_input: bool = False):
        """
        Mix fluids consisting of components from the AGA8 component list, based on their masses.
        Uses molecular weights from the initialized AGA8 equation of state.
        The function can take any number of compositions and corresponding masses, and will return the resulting composition and total mass of the mixture.

        Parameters
        ----------
        compositions : list
            A list of composition dictionaries, where each dictionary contains component names as keys 
            and mole percent or mole fraction as values. Components should be from the AGA8 component list:
            C1, N2, CO2, C2, C3, iC4, nC4, iC5, nC5, nC6, nC7, nC8, nC9, nC10, H2, O2, CO, H2O, H2S, He, Ar.
        mix_weights : list
            A list of masses [kg] corresponding to each composition. Must be the same length as compositions.
            Can include negative values for subtraction operations.
        check_input : bool, optional
            If True, raises exceptions for invalid inputs. If False, returns NaN values for invalid inputs.
            Default is False.

        Returns
        -------
        results : dict
            Dictionary containing:
            - 'composition': Dictionary with component names as keys and mole percent (0-100) as values.
            - 'total_mass': Total mass of the mixture [kg].

        Raises
        ------
        ValueError
            If check_input is True and any of the following occur:
            - Length of compositions and mix_weights lists don't match
            - Any component moles become negative after mixing (non-physical)
            - Total mass becomes negative after mixing
            - Invalid component names in compositions

        Examples
        --------
        >>> aga8 = AGA8('GERG-2008')
        >>> comp1 = {'C1': 90, 'C2': 10}
        >>> comp2 = {'C1': 80, 'C3': 20}
        >>> result = aga8.mix([comp1, comp2], [100, 50])
        >>> result['composition']
        {'C1': 86.67, 'C2': 6.67, 'C3': 6.67}
        >>> result['total_mass']
        150.0

        References
        ----------
        .. [1] AGA Report No. 8, Thermodynamic Properties of Natural Gas and Related Gases.
        """
        
        # Use molecular weights and component list from class initialization
        n_components = len(self.aga8_components)
        
        # Collect all unique components from the input compositions
        # This will be used for error return to only include components that were present in the inputs
        unique_components = set()
        for comp_dict in compositions:
            unique_components.update(comp_dict.keys())
        
        # Error return dictionary - only includes components present in input compositions
        results_error = {
            'composition': {comp: np.nan for comp in unique_components},
            'total_mass': np.nan
        }
        
        # Input validation
        n_compositions = len(compositions)
        n_weights = len(mix_weights)
        
        if check_input:
            if n_compositions != n_weights:
                raise ValueError('Length of compositions and mix_weights lists must be equal.')
            if n_compositions == 0:
                raise ValueError('At least one composition must be provided.')
        else:
            if n_compositions != n_weights:
                return results_error
            if n_compositions == 0:
                return results_error
        
        # Convert mix_weights to numpy array for vectorized operations
        mix_weights_array = np.array(mix_weights, dtype=np.float64)
        
        # Initialize numpy array to track moles of each component
        component_moles = np.zeros(n_components, dtype=np.float64)
        
        # Create composition matrix (n_compositions x n_components)
        comp_matrix = np.zeros((n_compositions, n_components), dtype=np.float64)
        
        # Fill composition matrix
        for i, comp_dict in enumerate(compositions):
            # Validate all components first
            for component in comp_dict.keys():
                if component not in self.component_indices:
                    if check_input:
                        raise ValueError(f'Invalid component: {component}. Must be one of the AGA8 components.')
                    else:
                        return results_error
            
            # Fill row in matrix
            for component, value in comp_dict.items():
                idx = self.component_indices[component]
                comp_matrix[i, idx] = value
        
        # Normalize each composition to mole fractions (vectorized)
        comp_sums = np.sum(comp_matrix, axis=1)
        
        # Check for zero sums
        if np.any(comp_sums == 0.0):
            if check_input:
                raise ValueError('Composition sum cannot be zero.')
            else:
                return results_error
        
        # Normalize to mole fractions (safe to divide since we checked for zeros above)
        comp_matrix_normalized = comp_matrix / comp_sums[:, np.newaxis]
        
        # Calculate average molecular weight for each composition (vectorized)
        avg_mw_array = np.dot(comp_matrix_normalized, self.molecular_weights)
        
        # Calculate total moles for each composition (vectorized)
        # Convert kg to g, then divide by g/mol
        total_moles_array = (mix_weights_array * 1000) / avg_mw_array
        
        # Calculate moles of each component for each composition (vectorized)
        moles_matrix = comp_matrix_normalized * total_moles_array[:, np.newaxis]
        
        # Sum moles across all compositions (vectorized)
        component_moles = np.sum(moles_matrix, axis=0)
        
        # Calculate total mass
        total_mass = np.sum(mix_weights_array)
        
        # Check for negative moles (non-physical)
        if check_input:
            if np.any(component_moles < 0):
                negative_indices = np.where(component_moles < 0)[0]
                negative_components = [self.aga8_components[i] for i in negative_indices]
                raise ValueError(f'Negative moles detected for components: {negative_components}. This is non-physical.')
            if total_mass < 0:
                raise ValueError(f'Total mass is negative ({total_mass} kg). This is non-physical.')
        else:
            if np.any(component_moles < 0) or total_mass < 0:
                return results_error
        
        # Calculate total moles
        total_moles_sum = np.sum(component_moles)
        
        # Handle case where total moles is zero
        if total_moles_sum == 0.0:
            if check_input:
                raise ValueError('Total moles is zero after mixing.')
            else:
                return results_error
        
        # Calculate mole fractions and convert to mole percent (vectorized)
        mole_fractions = component_moles / total_moles_sum
        mole_percents = mole_fractions * 100.0
        
        # Create result dictionary with only non-zero components
        # Use numpy boolean indexing for speed
        nonzero_mask = mole_percents > 0
        nonzero_indices = np.where(nonzero_mask)[0]
        
        result_composition = {
            self.aga8_components[idx]: float(mole_percents[idx]) 
            for idx in nonzero_indices
        }
        
        results = {
            'composition': result_composition,
            'total_mass': float(total_mass)
        }
        
        return results



def _pressure_unit_conversion(pressure_value, pressure_unit = 'bara'):
    """
    Convert a given pressure value to kilopascals (kPa).
    Parameters:
    pressure_value (float): The pressure value to be converted.
    pressure_unit (str): The unit of the pressure value. Supported units are:
                            'bara'  - Bar absolute (default)
                            'Pa'    - Pascal
                            'psi'   - Pounds per square inch
                            'psia'  - Pounds per square inch absolute
                            'psig'  - Pounds per square inch gauge
                            'barg'  - Bar gauge
                            'MPa'   - Megapascal
                            'kPa'   - Kilopascal
    Returns:
    float: The pressure value converted to kilopascals (kPa).
    Raises:
    Exception: If the provided pressure unit is not supported.
    """


    # Convert inputs to SI units, i.e. kPa
    if pressure_unit.lower() == 'bara':
        pressure = pressure_value * 100
    elif pressure_unit.lower() == 'pa':
        pressure = pressure_value / 1000
    elif pressure_unit.lower() == 'psi':
        pressure = pressure_value * 6.89476
    elif pressure_unit.lower() == 'psia':
        pressure = (pressure_value + 14.6959488) * 6.89476
    elif pressure_unit.lower() == 'psig':
        pressure = pressure_value * 6.89476 + 101.325
    elif pressure_unit.lower() == 'barg':
        pressure = pressure_value * 100 + 101.325
    elif pressure_unit.lower() == 'mpa':
        pressure = pressure_value * 1000
    elif pressure_unit.lower() == 'kpa':
        pressure = pressure_value
    else:
        raise Exception(f'Pressure unit "{pressure_unit}" not supported!')
    
    return pressure


def _temperature_unit_conversion(temperature_value, temperature_unit = 'C'):
    """
    Parameters
    ----------
    temperature_value : float
        The temperature value to be converted.
    temperature_unit : str, optional
        The unit of the temperature value. Supported units are 'C' for Celsius, 
        'F' for Fahrenheit, and 'K' for Kelvin. Defaults to 'C' (Celsius).
    Returns
    -------
    float
        The temperature value converted to Kelvin.
    Raises
    ------
    Exception
        If the provided temperature unit is not supported.
    """

    # Convert inputs to SI units, i.e. Kelvin
    if temperature_unit.lower() == 'c':
        temperature = temperature_value + 273.15
    elif temperature_unit.lower() == 'f':
        temperature = (temperature_value - 32) * 5 / 9 + 273.15
    elif temperature_unit.lower() == 'k':
        temperature = temperature_value
    else:
        raise Exception(f'Temperature unit "{temperature_unit}" not supported!')

    return temperature


def to_aga8_composition(composition: dict):
    """
    Convert a composition dictionary to an AGA8 Composition object.

    Parameters
    ----------
    composition : dict
        A dictionary containing the component names as keys and the mole fractions or mole percentages as values.

    Returns
    -------
    AGA8_COMPOSITION : pyaga8.Composition
        An AGA8 Composition object.
    aga8_composition_dict : dict
        A dictionary containing the AGA8 component names as keys and the mole fractions as values.
    """

    # Create AGA8 composition object
    AGA8_COMPOSITION = pyaga8.Composition()

    aga8_component_list = ['C1', 'N2', 'CO2', 'C2', 'C3', 'iC4', 'nC4', 'iC5', 'nC5', 'nC6', 'nC7', 'nC8', 'nC9', 'nC10', 'H2', 'O2', 'CO', 'H2O', 'H2S', 'He', 'Ar']

    aga8_composition_dict = {component : 0.0 for component in aga8_component_list}

    # Sum of input composition (used for normalization)
    composition_sum = sum(composition.values())

    # Component normalization and assignment to aga8 list
    for component, mole_percent in composition.items():
        mole_fraction_normalized = mole_percent / composition_sum

        comp_name = component.split(sep='-')[0]

        if comp_name[0] == 'C' and comp_name[1].isnumeric():

            Cn = int(comp_name[1:])

            #Components with carbon numbers from C6 to C9 are assigned to the corresponding normal alkane
            if Cn in [6,7,8,9]:
                aga8_composition_dict[f'nC{Cn}'] =  mole_fraction_normalized
            
            #Components with carbon number equal or greater than 10, is assigned to nC10
            elif Cn >= 10:
                aga8_composition_dict['nC10'] =  mole_fraction_normalized
            
            #Components with carbon numbers below C6 is assigned to the appropriate AGA8 component. For example C3 or iC4
            else:
                aga8_composition_dict[comp_name] = mole_fraction_normalized

        else:
            if comp_name in list(aga8_composition_dict.keys()):  # if the carbon number is not found, for example for C3, the
                # function looks for the component in the AGA8 fluid and adds the component
                aga8_composition_dict[comp_name] = mole_fraction_normalized
            else:
                raise Exception(f'Illegal component: {comp_name}')

    for component, mole_fraction in aga8_composition_dict.items():
        if component=='C1':
            AGA8_COMPOSITION.methane = mole_fraction
        elif component=='N2':
            AGA8_COMPOSITION.nitrogen = mole_fraction
        elif component=='CO2':
            AGA8_COMPOSITION.carbon_dioxide = mole_fraction
        elif component=='C2':
            AGA8_COMPOSITION.ethane = mole_fraction
        elif component=='C3':
            AGA8_COMPOSITION.propane = mole_fraction
        elif component=='iC4':
            AGA8_COMPOSITION.isobutane = mole_fraction
        elif component=='nC4':
            AGA8_COMPOSITION.n_butane = mole_fraction
        elif component=='iC5':
            AGA8_COMPOSITION.isopentane = mole_fraction
        elif component=='nC5':
            AGA8_COMPOSITION.n_pentane = mole_fraction
        elif component=='nC6':
            AGA8_COMPOSITION.hexane = mole_fraction
        elif component=='nC7':
            AGA8_COMPOSITION.heptane = mole_fraction
        elif component=='nC8':
            AGA8_COMPOSITION.octane = mole_fraction
        elif component=='nC9':
            AGA8_COMPOSITION.nonane = mole_fraction
        elif component=='nC10':
            AGA8_COMPOSITION.decane = mole_fraction
        elif component=='H2':
            AGA8_COMPOSITION.hydrogen = mole_fraction
        elif component=='O2':
            AGA8_COMPOSITION.oxygen = mole_fraction
        elif component=='CO':
            AGA8_COMPOSITION.carbon_monoxide = mole_fraction
        elif component=='H2O':
            AGA8_COMPOSITION.water = mole_fraction
        elif component=='H2S':
            AGA8_COMPOSITION.hydrogen_sulfide = mole_fraction
        elif component=='He':
            AGA8_COMPOSITION.helium = mole_fraction
        elif component=='Ar':
            AGA8_COMPOSITION.argon = mole_fraction

    return AGA8_COMPOSITION, aga8_composition_dict
