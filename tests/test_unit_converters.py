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

Note: Tests for unit_converters.py has been automatically generated using CoPilot.
"""

from pvtlib.unit_converters import *

def test_celsius_to_kelvin():
    assert celsius_to_kelvin(0) == 273.15
    assert celsius_to_kelvin(100) == 373.15

def test_kelvin_to_celsius():
    assert kelvin_to_celsius(273.15) == 0
    assert kelvin_to_celsius(373.15) == 100

def test_fahrenheit_to_kelvin():
    assert round(fahrenheit_to_kelvin(32), 2) == 273.15
    assert round(fahrenheit_to_kelvin(212), 2) == 373.15

def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(32) == 0
    assert fahrenheit_to_celsius(212) == 100

def test_celsius_to_rankine():
    assert round(celsius_to_rankine(0), 2) == 491.67
    assert round(celsius_to_rankine(100), 2) == 671.67

def test_barg_to_bara():
    assert barg_to_bara(1) == 2.01325
    assert barg_to_bara(0) == 1.01325

def test_bara_to_barg():
    assert round(bara_to_barg(2.01325),10) == 1.0
    assert round(bara_to_barg(1.01325),10) == 0.0

def test_bar_to_psi():
    assert round(bar_to_psi(1), 4) == 14.5038
    assert bar_to_psi(0) == 0

def test_kPa_to_Pa():
    assert kPa_to_Pa(1) == 1000
    assert kPa_to_Pa(0) == 0

def test_Pa_to_kPa():
    assert Pa_to_kPa(1000) == 1
    assert Pa_to_kPa(0) == 0

def test_MPa_to_Pa():
    assert MPa_to_Pa(1) == 1000000
    assert MPa_to_Pa(0) == 0

def test_Pa_to_MPa():
    assert Pa_to_MPa(1000000) == 1
    assert Pa_to_MPa(0) == 0

def test_Pa_to_bar():
    assert Pa_to_bar(100000) == 1
    assert Pa_to_bar(0) == 0

def test_bar_to_Pa():
    assert bar_to_Pa(1) == 100000
    assert bar_to_Pa(0) == 0

def test_barg_to_Pa():
    assert round(barg_to_Pa(1),10) == 201325.0
    assert round(barg_to_Pa(0),10) == 101325.0

def test_barg_to_kPa():
    assert round(barg_to_kPa(1), 3) == 201.325
    assert round(barg_to_kPa(0), 3) == 101.325

def test_Pa_to_barg():
    assert round(Pa_to_barg(201325),10) == 1.0
    assert round(Pa_to_barg(101325),10) == 0.0

def test_kPa_to_bar():
    assert kPa_to_bar(100) == 1
    assert kPa_to_bar(0) == 0

def test_bar_to_kPa():
    assert bar_to_kPa(1) == 100
    assert bar_to_kPa(0) == 0

def test_MPa_to_bar():
    assert MPa_to_bar(1) == 10
    assert MPa_to_bar(0) == 0

def test_bar_to_MPa():
    assert bar_to_MPa(10) == 1
    assert bar_to_MPa(0) == 0

def test_psi_to_bar():
    assert round(psi_to_bar(14.5038), 4) == 1
    assert psi_to_bar(0) == 0

def test_psi_to_Pa():
    assert round(psi_to_Pa(1), 5) == 6894.75729
    assert psi_to_Pa(0) == 0

def test_bar_to_mbar():
    assert bar_to_mbar(1) == 1000
    assert bar_to_mbar(0) == 0

def test_mbar_to_bar():
    assert mbar_to_bar(1000) == 1
    assert mbar_to_bar(0) == 0

def test_mbar_to_Pa():
    assert mbar_to_Pa(1) == 100
    assert mbar_to_Pa(0) == 0

def test_Pas_to_cP():
    assert Pas_to_cP(1) == 1000
    assert Pas_to_cP(0) == 0

def test_kgPerHour_to_kgPerSecond():
    assert kgPerHour_to_kgPerSecond(3600) == 1
    assert kgPerHour_to_kgPerSecond(0) == 0

def test_kgPerSecond_to_kgPerHour():
    assert kgPerSecond_to_kgPerHour(1) == 3600
    assert kgPerSecond_to_kgPerHour(0) == 0

def test_tonPerHour_to_kgPerHour():
    assert tonPerHour_to_kgPerHour(1) == 1000
    assert tonPerHour_to_kgPerHour(0) == 0

def test_kgPerHour_to_tonPerHour():
    assert kgPerHour_to_tonPerHour(1000) == 1
    assert kgPerHour_to_tonPerHour(0) == 0

def test_tonPerHour_to_kgPerSecond():
    assert round(tonPerHour_to_kgPerSecond(1), 5) == 0.27778
    assert tonPerHour_to_kgPerSecond(0) == 0

def test_kgPerSecond_to_tonPerHour():
    assert round(kgPerSecond_to_tonPerHour(1), 4) == 3.6
    assert kgPerSecond_to_tonPerHour(0) == 0

def test_kg_to_ton():
    assert kg_to_ton(1000) == 1
    assert kg_to_ton(0) == 0

def test_ton_to_kg():
    assert ton_to_kg(1) == 1000
    assert ton_to_kg(0) == 0

def test_g_to_ton():
    assert g_to_ton(1000000) == 1
    assert g_to_ton(0) == 0

def test_ton_to_g():
    assert ton_to_g(1) == 1000000
    assert ton_to_g(0) == 0

def test_kg_to_g():
    assert kg_to_g(1) == 1000
    assert kg_to_g(0) == 0

def test_g_to_kg():
    assert g_to_kg(1000) == 1
    assert g_to_kg(0) == 0

def test_kgperm3_to_gpercm3():
    assert kgperm3_to_gpercm3(1000) == 1
    assert kgperm3_to_gpercm3(0) == 0

def test_gpermol_to_kgperkmol():
    assert gpermol_to_kgperkmol(1) == 1
    assert gpermol_to_kgperkmol(0) == 0

def test_kgperkmol_to_gpermol():
    assert kgperkmol_to_gpermol(1) == 1
    assert kgperkmol_to_gpermol(0) == 0

def test_m3PerHour_to_m3PerSecond():
    assert m3PerHour_to_m3PerSecond(3600) == 1
    assert m3PerHour_to_m3PerSecond(0) == 0

def test_m3PerSecond_to_m3PerHour():
    assert m3PerSecond_to_m3PerHour(1) == 3600
    assert m3PerSecond_to_m3PerHour(0) == 0

def test_meter_to_feet():
    assert round(meter_to_feet(1), 7) == 3.2808399
    assert meter_to_feet(0) == 0

def test_feet_to_meter():
    assert round(feet_to_meter(3.2808399), 7) == 1
    assert feet_to_meter(0) == 0

def test_millimeter_to_feet():
    assert round(millimeter_to_feet(1000), 7) == 3.2808399
    assert millimeter_to_feet(0) == 0

def test_feet_to_millimeter():
    assert round(feet_to_millimeter(3.2808399), 7) == 1000
    assert feet_to_millimeter(0) == 0

def test_meter_to_millimeter():
    assert meter_to_millimeter(1) == 1000
    assert meter_to_millimeter(0) == 0

def test_millimeter_to_meter():
    assert millimeter_to_meter(1000) == 1
    assert millimeter_to_meter(0) == 0

def test_meter_to_inches():
    assert round(meter_to_inches(1), 7) == 39.3700787
    assert meter_to_inches(0) == 0

def test_inches_to_meter():
    assert round(inches_to_meter(39.3700787), 7) == 1
    assert inches_to_meter(0) == 0

def test_millimeter_to_inches():
    assert round(millimeter_to_inches(1000), 7) == 39.3700787
    assert millimeter_to_inches(0) == 0

def test_inches_to_millimeter():
    assert round(inches_to_millimeter(39.3700787), 7) == 1000
    assert inches_to_millimeter(0) == 0

def test_second_to_millisecond():
    assert second_to_millisecond(1) == 1000
    assert second_to_millisecond(0) == 0

def test_second_to_microsecond():
    assert second_to_microsecond(1) == 1000000
    assert second_to_microsecond(0) == 0

def test_millisecond_to_second():
    assert millisecond_to_second(1000) == 1
    assert millisecond_to_second(0) == 0

def test_microsecond_to_second():
    assert microsecond_to_second(1000000) == 1
    assert microsecond_to_second(0) == 0

def test_A_to_kA():
    assert A_to_kA(1000) == 1
    assert A_to_kA(0) == 0

def test_kA_to_A():
    assert kA_to_A(1) == 1000
    assert kA_to_A(0) == 0

def test_mA_to_A():
    assert mA_to_A(1000) == 1
    assert mA_to_A(0) == 0

def test_A_to_mA():
    assert A_to_mA(1) == 1000
    assert A_to_mA(0) == 0

def test_V_to_kV():
    assert V_to_kV(1000) == 1
    assert V_to_kV(0) == 0

def test_kV_to_V():
    assert kV_to_V(1) == 1000
    assert kV_to_V(0) == 0

def test_mV_to_V():
    assert mV_to_V(1000) == 1
    assert mV_to_V(0) == 0

def test_V_to_mV():
    assert V_to_mV(1) == 1000
    assert V_to_mV(0) == 0

def test_Ohm_to_milliOhm():
    assert Ohm_to_milliOhm(1) == 1000
    assert Ohm_to_milliOhm(0) == 0

def test_milliOhm_to_Ohm():
    assert milliOhm_to_Ohm(1000) == 1
    assert milliOhm_to_Ohm(0) == 0

def test_Ohm_to_microOhm():
    assert Ohm_to_microOhm(1) == 1000000
    assert Ohm_to_microOhm(0) == 0

def test_microOhm_to_Ohm():
    assert microOhm_to_Ohm(1000000) == 1
    assert microOhm_to_Ohm(0) == 0

def test_microOhm_to_Ohm_new():
    assert microOhm_to_Ohm_new(1000000) == 1
    assert microOhm_to_Ohm_new(0) == 0

def test_VA_to_kVA():
    assert VA_to_kVA(1000) == 1
    assert VA_to_kVA(0) == 0

def test_kVA_to_VA():
    assert kVA_to_VA(1) == 1000
    assert kVA_to_VA(0) == 0

def test_mole_to_kmole():
    assert mole_to_kmole(1000) == 1
    assert mole_to_kmole(0) == 0

def test_kmole_to_mole():
    assert kmole_to_mole(1) == 1000
    assert kmole_to_mole(0) == 0

def test_W_to_kW():
    assert W_to_kW(1000) == 1
    assert W_to_kW(0) == 0

def test_kW_to_W():
    assert kW_to_W(1) == 1000
    assert kW_to_W(0) == 0

def test_W_to_MW():
    assert W_to_MW(1000000) == 1
    assert W_to_MW(0) == 0

def test_MW_to_W():
    assert MW_to_W(1) == 1000000
    assert MW_to_W(0) == 0

def test_kW_to_kiloJoulePerHour():
    assert kW_to_kiloJoulePerHour(1) == 3600
    assert kW_to_kiloJoulePerHour(0) == 0

def test_kiloJoulePerHour_to_kW():
    assert kiloJoulePerHour_to_kW(3600) == 1
    assert kiloJoulePerHour_to_kW(0) == 0

def test_W_to_kiloJoulePerHour():
    assert W_to_kiloJoulePerHour(1000) == 3600
    assert W_to_kiloJoulePerHour(0) == 0

def test_kiloJoulePerHour_to_W():
    assert kiloJoulePerHour_to_W(3600) == 1000
    assert kiloJoulePerHour_to_W(0) == 0

def test_kiloJoulePerkg_to_JoulePerkg():
    assert kiloJoulePerkg_to_JoulePerkg(1) == 1000
    assert kiloJoulePerkg_to_JoulePerkg(0) == 0

def test_JoulePerkg_to_kiloJoulePerkg():
    assert JoulePerkg_to_kiloJoulePerkg(1000) == 1
    assert JoulePerkg_to_kiloJoulePerkg(0) == 0

def test_kiloJoulePerkg_to_meter():
    assert round(kiloJoulePerkg_to_meter(1), 4) == 101.9368
    assert kiloJoulePerkg_to_meter(0) == 0

def test_meter_to_kiloJoulePerkg():
    assert round(meter_to_kiloJoulePerkg(101.9368), 4) == 1
    assert meter_to_kiloJoulePerkg(0) == 0

def test_metersPerSecond_to_kilometersPerHour():
    assert metersPerSecond_to_kilometersPerHour(1) == 3.6
    assert metersPerSecond_to_kilometersPerHour(0) == 0

def test_kilometersPerHour_to_metersPerSecond():
    assert kilometersPerHour_to_metersPerSecond(3.6) == 1
    assert kilometersPerHour_to_metersPerSecond(0) == 0

def test_metersPerSecond_to_milesPerHour():
    assert round(metersPerSecond_to_milesPerHour(1), 8) == 2.23693629
    assert metersPerSecond_to_milesPerHour(0) == 0

def test_milesPerHour_to_metersPerSecond():
    assert round(milesPerHour_to_metersPerSecond(2.23693629), 8) == 1
    assert milesPerHour_to_metersPerSecond(0) == 0

def test_radians_to_degrees():
    assert round(radians_to_degrees(3.14159265359),10) == 180.0
    assert radians_to_degrees(0) == 0

def test_degrees_to_radians():
    assert round(degrees_to_radians(180), 8) == 3.14159265
    assert degrees_to_radians(0) == 0

def test_mol_per_liter_to_mol_per_m3():
    assert mol_per_liter_to_mol_per_m3(1) == 1000
    assert mol_per_liter_to_mol_per_m3(0) == 0

def test_liter_per_mol_to_m3_per_mol():
    assert liter_per_mol_to_m3_per_mol(1) == 0.001
    assert liter_per_mol_to_m3_per_mol(0) == 0