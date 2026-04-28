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

import math

# Temperature
def celsius_to_kelvin(celsius):
    '''Convert temperature from Celsius to Kelvin [°C → K].'''
    kelvin = celsius+273.15
    return kelvin


def kelvin_to_celsius(kelvin):
    '''Convert temperature from Kelvin to Celsius [K → °C].'''
    celsius = kelvin-273.15
    return celsius


def fahrenheit_to_kelvin(fahrenheit):
    '''Convert temperature from Fahrenheit to Kelvin [°F → K].'''
    kelvin = (fahrenheit+459.67)*5/9
    return kelvin


def fahrenheit_to_celsius(fahrenheit):
    '''Convert temperature from Fahrenheit to Celsius [°F → °C].'''
    celsius = (fahrenheit-32)*5/9
    return celsius

def celsius_to_rankine(celsius):
    '''Convert temperature from Celsius to Rankine [°C → °R].'''
    rankine = (celsius+273.15)*9/5
    return rankine

# Pressure
def barg_to_bara(barg, P_atm=1.01325):
    '''Convert pressure from bar gauge to bar absolute [barg → bara]. P_atm defaults to 1.01325 bar.'''
    bara = barg + P_atm
    return bara


def bara_to_barg(bara, P_atm=1.01325):
    '''Convert pressure from bar absolute to bar gauge [bara → barg]. P_atm defaults to 1.01325 bar.'''
    barg = bara-P_atm
    return barg

def bar_to_psi(bar):
    '''Convert pressure from bar to pounds per square inch [bar → psi].'''
    psi = bar*14.503773773
    return psi

def kPa_to_Pa(kPa):
    '''Convert pressure from kilopascal to pascal [kPa → Pa].'''
    Pa = kPa*1000
    return Pa


def Pa_to_kPa(Pa):
    '''Convert pressure from pascal to kilopascal [Pa → kPa].'''
    kPa = Pa/1000
    return kPa


def MPa_to_Pa(MPa):
    '''Convert pressure from megapascal to pascal [MPa → Pa].'''
    Pa = MPa*1000000
    return Pa


def Pa_to_MPa(Pa):
    '''Convert pressure from pascal to megapascal [Pa → MPa].'''
    MPa = Pa/1000000
    return MPa


def Pa_to_bar(Pa):
    '''Convert pressure from pascal to bar [Pa → bar].'''
    bar = Pa/100000
    return bar


def bar_to_Pa(bar):
    '''Convert pressure from bar to pascal [bar → Pa].'''
    Pa = bar*100000
    return Pa


def barg_to_Pa(barg, P_atm=1.01325):
    '''Convert pressure from bar gauge to pascal [barg → Pa]. P_atm defaults to 1.01325 bar.'''
    Pa = (barg+P_atm)*100000
    return Pa


def Pa_to_barg(Pa, P_atm=1.01325):
    '''Convert pressure from pascal to bar gauge [Pa → barg]. P_atm defaults to 1.01325 bar.'''
    barg = (Pa/100000)-P_atm
    return barg


def kPa_to_bar(kPa):
    '''Convert pressure from kilopascal to bar [kPa → bar].'''
    bar = kPa/100
    return bar


def bar_to_kPa(bar):
    '''Convert pressure from bar to kilopascal [bar → kPa].'''
    kPa = bar*100
    return kPa

def barg_to_kPa(barg, P_atm=1.01325):
    '''Convert pressure from bar gauge to kilopascal [barg → kPa]. P_atm defaults to 1.01325 bar.'''
    bara = barg_to_bara(barg,P_atm)
    kPa = bara*100
    return kPa

def MPa_to_bar(MPa):
    '''Convert pressure from megapascal to bar [MPa → bar].'''
    bar = MPa*10
    return bar


def bar_to_MPa(bar):
    '''Convert pressure from bar to megapascal [bar → MPa].'''
    MPa = bar/10
    return MPa

def psi_to_bar(psi):
    '''Convert pressure from pounds per square inch to bar [psi → bar].'''
    bar = psi*0.0689475729
    return bar


def psi_to_Pa(psi):
    '''Convert pressure from pounds per square inch to pascal [psi → Pa].'''
    Pa = psi*6894.75729
    return Pa


def bar_to_mbar(bar):
    '''Convert pressure from bar to millibar [bar → mbar].'''
    mbar = bar*1000
    return mbar

def mbar_to_bar(mbar):
    '''Convert pressure from millibar to bar [mbar → bar].'''
    bar = mbar/1000
    return bar

def mbar_to_Pa(mbar):
    '''Convert pressure from millibar to pascal [mbar → Pa].'''
    Pa = mbar*100
    return Pa


#Viscosity
def Pas_to_cP(Pas):
    '''Convert dynamic viscosity from pascal-second to centipoise [Pa·s → cP].'''
    cP = Pas*1000
    return cP


# Mass Flow
def kgPerHour_to_kgPerSecond(kgPerHour):
    '''Convert mass flow rate from kg/h to kg/s [kg/h → kg/s].'''
    kgPerSecond = kgPerHour/3600
    return kgPerSecond


def kgPerSecond_to_kgPerHour(kgPerSecond):
    '''Convert mass flow rate from kg/s to kg/h [kg/s → kg/h].'''
    kgPerHour = kgPerSecond*3600
    return kgPerHour


def tonPerHour_to_kgPerHour(tonPerHour):
    '''Convert mass flow rate from tonne/h to kg/h [t/h → kg/h].'''
    kgPerHour = tonPerHour*1000
    return kgPerHour


def kgPerHour_to_tonPerHour(kgPerHour):
    '''Convert mass flow rate from kg/h to tonne/h [kg/h → t/h].'''
    tonPerHour = kgPerHour/1000
    return tonPerHour


def tonPerHour_to_kgPerSecond(tonPerHour):
    '''Convert mass flow rate from tonne/h to kg/s [t/h → kg/s].'''
    kgPerSecond = tonPerHour*1000/3600
    return kgPerSecond


def kgPerSecond_to_tonPerHour(kgPerSecond):
    '''Convert mass flow rate from kg/s to tonne/h [kg/s → t/h].'''
    tonPerHour = kgPerSecond*3600/1000
    return tonPerHour

# Mass
def kg_to_ton(kg):
    '''Convert mass from kilogram to tonne [kg → t].'''
    ton = kg/1000
    return ton


def ton_to_kg(ton):
    '''Convert mass from tonne to kilogram [t → kg].'''
    kg = ton*1000
    return kg


def g_to_ton(g):
    '''Convert mass from gram to tonne [g → t].'''
    ton = g/1000000
    return ton


def ton_to_g(ton):
    '''Convert mass from tonne to gram [t → g].'''
    g = ton*1000000
    return g


def kg_to_g(kg):
    '''Convert mass from kilogram to gram [kg → g].'''
    g = kg*1000
    return g


def g_to_kg(g):
    '''Convert mass from gram to kilogram [g → kg].'''
    kg = g/1000
    return kg

# Density
def kgperm3_to_gpercm3(kgperm3):
    '''Convert density from kg/m³ to g/cm³ [kg/m³ → g/cm³].'''
    gpercm3 = kgperm3/1000
    return gpercm3

# Molar mass: kg/mol, g/mol, kg/kmol
def gpermol_to_kgperkmol(gpermol):
    '''Convert molar mass from g/mol to kg/kmol [g/mol → kg/kmol]. Values are numerically equal.'''
    kgperkmol = gpermol
    return kgperkmol


def kgperkmol_to_gpermol(kgperkmol):
    '''Convert molar mass from kg/kmol to g/mol [kg/kmol → g/mol]. Values are numerically equal.'''
    gpermol = kgperkmol
    return gpermol


# Volume flow: m3/h, m3/s
def m3PerHour_to_m3PerSecond(m3PerHour):
    '''Convert volumetric flow rate from m³/h to m³/s [m³/h → m³/s].'''
    m3PerSecond = m3PerHour/3600
    return m3PerSecond


def m3PerSecond_to_m3PerHour(m3PerSecond):
    '''Convert volumetric flow rate from m³/s to m³/h [m³/s → m³/h].'''
    m3PerHour = m3PerSecond*3600
    return m3PerHour


# Length: m, mm, in, feet
def meter_to_feet(meter):
    '''Convert length from metre to feet [m → ft].'''
    feet = meter*3.2808399
    return feet


def feet_to_meter(feet):
    '''Convert length from feet to metre [ft → m].'''
    meter = feet/3.2808399
    return meter


def millimeter_to_feet(millimeter):
    '''Convert length from millimetre to feet [mm → ft].'''
    feet = millimeter*3.2808399/1000
    return feet


def feet_to_millimeter(feet):
    '''Convert length from feet to millimetre [ft → mm].'''
    millimeter = feet/3.2808399*1000
    return millimeter


def meter_to_millimeter(meter):
    '''Convert length from metre to millimetre [m → mm].'''
    millimeter = meter*1000
    return millimeter


def millimeter_to_meter(millimeter):
    '''Convert length from millimetre to metre [mm → m].'''
    meter = millimeter/1000
    return meter


def meter_to_inches(meter):
    '''Convert length from metre to inches [m → in].'''
    inches = meter*39.3700787
    return inches


def inches_to_meter(inches):
    '''Convert length from inches to metre [in → m].'''
    meter = inches/39.3700787
    return meter


def millimeter_to_inches(millimeter):
    '''Convert length from millimetre to inches [mm → in].'''
    inches = millimeter*39.3700787/1000
    return inches


def inches_to_millimeter(inches):
    '''Convert length from inches to millimetre [in → mm].'''
    millimeter = inches/39.3700787*1000
    return millimeter


# Time: microsecond, second, millisecond
def second_to_millisecond(second):
    '''Convert time from second to millisecond [s → ms].'''
    millisecond = second*1000
    return millisecond


def second_to_microsecond(second):
    '''Convert time from second to microsecond [s → μs].'''
    microsecond = second*1000000
    return microsecond


def millisecond_to_second(millisecond):
    '''Convert time from millisecond to second [ms → s].'''
    second = millisecond/1000
    return second


def microsecond_to_second(microsecond):
    '''Convert time from microsecond to second [μs → s].'''
    second = microsecond/1000000
    return second


# Electro: A, V, Ohm
def A_to_kA(A):
    '''Convert electric current from ampere to kiloampere [A → kA].'''
    kA = A/1000
    return kA


def kA_to_A(kA):
    '''Convert electric current from kiloampere to ampere [kA → A].'''
    A = kA*1000
    return A


def mA_to_A(mA):
    '''Convert electric current from milliampere to ampere [mA → A].'''
    A = mA/1000
    return A


def A_to_mA(A):
    '''Convert electric current from ampere to milliampere [A → mA].'''
    mA = A*1000
    return mA


def V_to_kV(V):
    '''Convert voltage from volt to kilovolt [V → kV].'''
    kV = V/1000
    return kV


def kV_to_V(kV):
    '''Convert voltage from kilovolt to volt [kV → V].'''
    V = kV*1000
    return V


def mV_to_V(mV):
    '''Convert voltage from millivolt to volt [mV → V].'''
    V = mV/1000
    return V


def V_to_mV(V):
    '''Convert voltage from volt to millivolt [V → mV].'''
    mV = V*1000
    return mV


def Ohm_to_milliOhm(Ohm):
    '''Convert electrical resistance from ohm to milliohm [Ω → mΩ].'''
    milliOhm = Ohm*1000
    return milliOhm


def milliOhm_to_Ohm(milliOhm):
    '''Convert electrical resistance from milliohm to ohm [mΩ → Ω].'''
    Ohm = milliOhm/1000
    return Ohm


def Ohm_to_microOhm(Ohm):
    '''Convert electrical resistance from ohm to microohm [Ω → μΩ].'''
    microOhm = Ohm*1000000
    return microOhm


def microOhm_to_Ohm(microOhm):
    '''Convert electrical resistance from microohm to ohm [μΩ → Ω].'''
    Ohm = microOhm/1000000
    return Ohm


def VA_to_kVA(VA):
    '''Convert apparent power from volt-ampere to kilovolt-ampere [VA → kVA].'''
    kVA = VA/1000
    return kVA


def kVA_to_VA(kVA):
    '''Convert apparent power from kilovolt-ampere to volt-ampere [kVA → VA].'''
    VA = kVA*1000
    return VA


# Amount: mole, kmole
def mole_to_kmole(mole):
    '''Convert amount of substance from mole to kilomole [mol → kmol].'''
    kmole = mole/1000
    return kmole


def kmole_to_mole(kmole):
    '''Convert amount of substance from kilomole to mole [kmol → mol].'''
    mole = kmole*1000
    return mole

# Energy: W, kW, kJ/h, kJ/kg, meter
def W_to_kW(W):
    '''Convert power from watt to kilowatt [W → kW].'''
    kW = W/1000
    return kW


def kW_to_W(kW):
    '''Convert power from kilowatt to watt [kW → W].'''
    W = kW*1000
    return W


def W_to_MW(W):
    '''Convert power from watt to megawatt [W → MW].'''
    MW = W/1000000
    return MW


def MW_to_W(MW):
    '''Convert power from megawatt to watt [MW → W].'''
    W = MW*1000000
    return W


def kW_to_kiloJoulePerHour(kW):
    '''Convert power from kilowatt to kilojoule per hour [kW → kJ/h].'''
    kiloJoulePerHour = kW*3600
    return kiloJoulePerHour


def kiloJoulePerHour_to_kW(kiloJoulePerHour):
    '''Convert power from kilojoule per hour to kilowatt [kJ/h → kW].'''
    kW = kiloJoulePerHour/3600
    return kW


def W_to_kiloJoulePerHour(W):
    '''Convert power from watt to kilojoule per hour [W → kJ/h].'''
    kiloJoulePerHour = W*3600/1000
    return kiloJoulePerHour


def kiloJoulePerHour_to_W(kiloJoulePerHour):
    '''Convert power from kilojoule per hour to watt [kJ/h → W].'''
    W = kiloJoulePerHour/3600*1000
    return W


def kiloJoulePerkg_to_JoulePerkg(kiloJoulePerkg):
    '''Convert specific energy from kJ/kg to J/kg [kJ/kg → J/kg].'''
    JoulePerkg = kiloJoulePerkg*1000
    return JoulePerkg


def JoulePerkg_to_kiloJoulePerkg(JoulePerkg):
    '''Convert specific energy from J/kg to kJ/kg [J/kg → kJ/kg].'''
    kiloJoulePerkg = JoulePerkg/1000
    return kiloJoulePerkg


def kiloJoulePerkg_to_meter(kiloJoulePerkg):
    '''Convert specific energy from kJ/kg to hydraulic head in metres [kJ/kg → m], using g = 9.81 m/s².'''
    meter = kiloJoulePerkg*1000/9.81
    return meter


def meter_to_kiloJoulePerkg(meter):
    '''Convert hydraulic head in metres to specific energy in kJ/kg [m → kJ/kg], using g = 9.81 m/s².'''
    kiloJoulePerkg = meter/1000*9.81
    return kiloJoulePerkg

# Velocity: m/s, km/h, mph
def metersPerSecond_to_kilometersPerHour(metersPerSecond):
    '''Convert velocity from m/s to km/h [m/s → km/h].'''
    kilometersPerHour = metersPerSecond*3600/1000
    return kilometersPerHour


def kilometersPerHour_to_metersPerSecond(kilometersPerHour):
    '''Convert velocity from km/h to m/s [km/h → m/s].'''
    metersPerSecond = kilometersPerHour/3600*1000
    return metersPerSecond


def metersPerSecond_to_milesPerHour(metersPerSecond):
    '''Convert velocity from m/s to miles per hour [m/s → mph].'''
    milesPerHour = metersPerSecond*2.23693629
    return milesPerHour


def milesPerHour_to_metersPerSecond(milesPerHour):
    '''Convert velocity from miles per hour to m/s [mph → m/s].'''
    metersPerSecond = milesPerHour/2.23693629
    return metersPerSecond

# Angles: Radians, degrees


def radians_to_degrees(radians):
    '''Convert angle from radians to degrees [rad → °].'''
    degrees = radians*180/math.pi
    return degrees

def degrees_to_radians(degrees):
    '''Convert angle from degrees to radians [° → rad].'''
    radians = degrees/180*math.pi
    return radians


def mol_per_liter_to_mol_per_m3(mol_per_liter):
    '''Convert molar concentration from mol/L to mol/m³ [mol/L → mol/m³].'''
    mol_per_m3 = mol_per_liter * 1000
    return mol_per_m3

def liter_per_mol_to_m3_per_mol(liter_per_mol):
    '''Convert molar volume from L/mol to m³/mol [L/mol → m³/mol].'''
    m3_per_mol = 0.001 * liter_per_mol
    return m3_per_mol