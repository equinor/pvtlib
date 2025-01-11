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


# Temperature
def celsius_to_kelvin(celsius):
    kelvin = celsius+273.15
    return kelvin


def kelvin_to_celsius(kelvin):
    celsius = kelvin-273.15
    return celsius


def fahrenheit_to_kelvin(fahrenheit):
    kelvin = (fahrenheit+459.67)*5/9
    return kelvin


def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit-32)*5/9
    return celsius

def celsius_to_rankine(celsius):
    rankine = (celsius+273.15)*9/5
    return rankine

# Pressure
def barg_to_bara(barg, P_atm=1.01325):
    bara = barg + P_atm
    return bara


def bara_to_barg(bara, P_atm=1.01325):
    barg = bara-P_atm
    return barg

def bar_to_psi(bar):
    psi = bar*14.503773773
    return psi

def kPa_to_Pa(kPa):
    Pa = kPa*1000
    return Pa


def Pa_to_kPa(Pa):
    kPa = Pa/1000
    return kPa


def MPa_to_Pa(MPa):
    Pa = MPa*1000000
    return Pa


def Pa_to_MPa(Pa):
    MPa = Pa/1000000
    return MPa


def Pa_to_bar(Pa):
    bar = Pa/100000
    return bar


def bar_to_Pa(bar):
    Pa = bar*100000
    return Pa


def barg_to_Pa(barg, P_atm=1.01325):
    Pa = (barg+P_atm)*100000
    return Pa


def barg_to_kPa(barg:float, atm=1.01325):
    return (barg + atm) * 10 ** 5 / 1000


def Pa_to_barg(Pa, P_atm=1.01325):
    barg = (Pa/100000)-P_atm
    return barg


def kPa_to_bar(kPa):
    bar = kPa/100
    return bar


def bar_to_kPa(bar):
    kPa = bar*100
    return kPa

def barg_to_kPa(barg, P_atm=1.01325):
    bara = barg_to_bara(barg,P_atm)
    kPa = bara*100
    return kPa

def MPa_to_bar(MPa):
    bar = MPa*10
    return bar


def bar_to_MPa(bar):
    MPa = bar/10
    return MPa

def psi_to_bar(psi):
    bar = psi*0.0689475729
    return bar


def psi_to_Pa(psi):
    Pa = psi*6894.75729
    return Pa


def bar_to_mbar(bar):
    mbar = bar*1000
    return mbar

def mbar_to_bar(mbar):
    bar = mbar/1000
    return bar

def mbar_to_Pa(mbar):
    Pa = mbar*100
    return Pa


#Viscosity
def Pas_to_cP(Pas):
    cP = Pas*1000
    return cP


# Mass Flow
def kgPerHour_to_kgPerSecond(kgPerHour):
    kgPerSecond = kgPerHour/3600
    return kgPerSecond


def kgPerSecond_to_kgPerHour(kgPerSecond):
    kgPerHour = kgPerSecond*3600
    return kgPerHour


def tonPerHour_to_kgPerHour(tonPerHour):
    kgPerHour = tonPerHour*1000
    return kgPerHour


def kgPerHour_to_tonPerHour(kgPerHour):
    tonPerHour = kgPerHour/1000
    return tonPerHour


def tonPerHour_to_kgPerSecond(tonPerHour):
    kgPerSecond = tonPerHour*1000/3600
    return kgPerSecond


def kgPerSecond_to_tonPerHour(kgPerSecond):
    tonPerHour = kgPerSecond*3600/1000
    return tonPerHour

# Mass
def kg_to_ton(kg):
    ton = kg/1000
    return ton


def ton_to_kg(ton):
    kg = ton*1000
    return kg


def g_to_ton(g):
    ton = g/1000000
    return ton


def ton_to_g(ton):
    g = ton*1000000
    return g


def kg_to_g(kg):
    g = kg*1000
    return g


def g_to_kg(g):
    kg = g/1000
    return kg

# Density
def kgperm3_to_gpercm3(kgperm3):
    gpercm3 = kgperm3/1000
    return gpercm3

# Molar mass: kg/mol, g/mol, kg/kmol
def gpermol_to_kgperkmol(gpermol):
    kgperkmol = gpermol
    return kgperkmol


def kgperkmol_to_gpermol(kgperkmol):
    gpermol = kgperkmol
    return gpermol


# Volume flow: m3/h, m3/s
def m3PerHour_to_m3PerSecond(m3PerHour):
    m3PerSecond = m3PerHour/3600
    return m3PerSecond


def m3PerSecond_to_m3PerHour(m3PerSecond):
    m3PerHour = m3PerSecond*3600
    return m3PerHour


# Length: m, mm, in, feet
def meter_to_feet(meter):
    feet = meter*3.2808399
    return feet


def feet_to_meter(feet):
    meter = feet/3.2808399
    return meter


def millimeter_to_feet(millimeter):
    feet = millimeter*3.2808399/1000
    return feet


def feet_to_millimeter(feet):
    millimeter = feet/3.2808399*1000
    return millimeter


def meter_to_millimeter(meter):
    millimeter = meter*1000
    return millimeter


def millimeter_to_meter(millimeter):
    meter = millimeter/1000
    return meter


def meter_to_inches(meter):
    inches = meter*39.3700787
    return inches


def inches_to_meter(inches):
    meter = inches/39.3700787
    return meter


def millimeter_to_inches(millimeter):
    inches = millimeter*39.3700787/1000
    return inches


def inches_to_millimeter(inches):
    millimeter = inches/39.3700787*1000
    return millimeter


# Time: microsecond, second, millisecond
def second_to_millisecond(second):
    millisecond = second*1000
    return millisecond


def second_to_microsecond(second):
    microsecond = second*1000000
    return microsecond


def millisecond_to_second(millisecond):
    second = millisecond/1000
    return second


def microsecond_to_second(microsecond):
    second = microsecond/1000000
    return second


# Electro: A, V, Ohm
def A_to_kA(A):
    kA = A/1000
    return kA


def kA_to_A(kA):
    A = kA*1000
    return A


def mA_to_A(mA):
    A = mA/1000
    return A


def A_to_mA(A):
    mA = A*1000
    return mA


def V_to_kV(V):
    kV = V/1000
    return kV


def kV_to_V(kV):
    V = kV*1000
    return V


def mV_to_V(mV):
    V = mV/1000
    return V


def V_to_mV(V):
    mV = V*1000
    return mV


def Ohm_to_milliOhm(Ohm):
    milliOhm = Ohm*1000
    return milliOhm


def milliOhm_to_Ohm(milliOhm):
    Ohm = milliOhm/1000
    return Ohm


def Ohm_to_microOhm(Ohm):
    microOhm = Ohm*1000000
    return microOhm


def microOhm_to_Ohm(microOhm):
    Ohm = microOhm/1000000
    return Ohm


def microOhm_to_Ohm_new(microOhm):
    Ohm = microOhm/1000000
    return Ohm


def VA_to_kVA(VA):
    kVA = VA/1000
    return kVA


def kVA_to_VA(kVA):
    VA = kVA*1000
    return VA


# Amount: mole, kmole
def mole_to_kmole(mole):
    kmole = mole/1000
    return kmole


def kmole_to_mole(kmole):
    mole = kmole*1000
    return mole

# Energy: W, kW, kJ/h, kJ/kg, meter
def W_to_kW(W):
    kW = W/1000
    return kW


def kW_to_W(kW):
    W = kW*1000
    return W


def W_to_MW(W):
    MW = W/1000000
    return MW


def MW_to_W(MW):
    W = MW*1000000
    return W


def kW_to_kiloJoulePerHour(kW):
    kiloJoulePerHour = kW*3600
    return kiloJoulePerHour


def kiloJoulePerHour_to_kW(kiloJoulePerHour):
    kW = kiloJoulePerHour/3600
    return kW


def W_to_kiloJoulePerHour(W):
    kiloJoulePerHour = W*3600/1000
    return kiloJoulePerHour


def kiloJoulePerHour_to_W(kiloJoulePerHour):
    W = kiloJoulePerHour/3600*1000
    return W


def kiloJoulePerkg_to_JoulePerkg(kiloJoulePerkg):
    JoulePerkg = kiloJoulePerkg*1000
    return JoulePerkg


def JoulePerkg_to_kiloJoulePerkg(JoulePerkg):
    kiloJoulePerkg = JoulePerkg/1000
    return kiloJoulePerkg


def kiloJoulePerkg_to_meter(kiloJoulePerkg):
    meter = kiloJoulePerkg*1000/9.81
    return meter


def meter_to_kiloJoulePerkg(meter):
    kiloJoulePerkg = meter/1000*9.81
    return kiloJoulePerkg

# Velocity: m/s, km/h, mph
def metersPerSecond_to_kilometersPerHour(metersPerSecond):
    kilometersPerHour = metersPerSecond*3600/1000
    return kilometersPerHour


def kilometersPerHour_to_metersPerSecond(kilometersPerHour):
    metersPerSecond = kilometersPerHour/3600*1000
    return metersPerSecond


def metersPerSecond_to_milesPerHour(metersPerSecond):
    milesPerHour = metersPerSecond*2.23693629
    return milesPerHour


def milesPerHour_to_metersPerSecond(milesPerHour):
    metersPerSecond = milesPerHour/2.23693629
    return metersPerSecond

# Angles: Radians, degrees


def radians_to_degrees(radians):
    degrees = radians*180/3.14159265359
    return degrees

def degrees_to_radians(degrees):
    radians = degrees/180*3.14159265359
    return radians


def mol_per_liter_to_mol_per_m3(mol_per_liter):
    mol_per_m3 = mol_per_liter * 1000
    return mol_per_m3

def liter_per_mol_to_m3_per_mol(liter_per_mol):
    m3_per_mol = 0.001 * liter_per_mol
    return m3_per_mol