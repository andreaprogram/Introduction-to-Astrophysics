# -*- coding: utf-8 -*-
"""
Created on Mon May 19 18:26:01 2025

@author: andrea
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# SIMULATION OF AN ANALEMMA VIEWED FROM DIFFERENT PLANETS OF THE SOLAR SYSTEM
# DATA INPUTS------------------------------------------------

#(e, epsilon, T, P) for each planet
#parameters = [[ 0.2056, np.radians(0.034), 87.968,  np.radians(167.45645)] ,\
#              [0.0935 , np.radians(25.19), 686.972, np.radians(66.10) ] , \
#              [0.0487, np.radians(3.13), 4330.595 , np.radians(104.75385)] , \
#              [ 0.0520 , np.radians(26.73), 10746.940, np.radians(182.43194)]] 


planet_data = {
    "Earth": {
        "e": 0.0176,
        "epsilon": np.radians(23.45),
        "T": 365.242,
        "P": np.radians(12.94),
        "phi": np.radians(41.505789),
        "day": 24
    },
    "Mercury": {
        "e": 0.2056,
        "epsilon": np.radians(0.034),
        "T": 87.968,
        "P": np.radians(0),
        "phi": np.radians(41.505789),
        "day": 4222.6
    },
    "Mars": {
        "e": 0.0935,
        "epsilon": np.radians(25.19),
        "T": 686.972,
        "P": np.radians(66.10),
        "phi": np.radians(41.505789),
        "day": 24.6597
    },
    "Jupiter": {
        "e": 0.0487,
        "epsilon": np.radians(3.13),
        "T": 4330.595,
        "P": np.radians(104.75385),
        "phi": np.radians(41.505789),
        "day": 9.9259
    },
    "Saturn": {
        "e": 0.0520,
        "epsilon": np.radians(26.73),
        "T": 10746.940,
        "P": np.radians(182.43194),
        "phi": np.radians(92.86),
        "day": 10.656
    }
}

# in here, we choose the planet for which we want to see the analema from

planet = planet_data["Jupiter"]
e = planet["e"]
epsilon = planet["epsilon"]
T = planet["T"]
P = planet["P"]
phi = planet["phi"]
day = planet["day"]
# EQUATIONS--------------------------------------------------
def Mean_anomaly(N): # Mean anomaly for day N
    return 2*np.pi*(N)/T

def EOT(Ma, ecc, tilt):  # Equation Of Time in minutes
    return -( -2*ecc*np.sin(Ma)-(np.tan(tilt/2))**2 * np.sin(2*(Ma+P)) )*((day*60)/(2*np.pi))  
 #in minutes

def delta(N): #Sun's declination
    return -epsilon * np.cos((2*np.pi*(N))/T)

def altitude(HA, d): #Sun's altitude
    return np.arcsin(np.sin(phi)*np.sin(d) + np.cos(phi)*np.cos(d)*np.cos(HA))

def azimuth(d, h, HA): #Sun's azimut
    cosA = (np.sin(d) - np.sin(phi) * np.sin(h)) / (np.cos(phi) * np.cos(h))
    cosA = np.clip(cosA, -1, 1)
    A = np.arccos(cosA)
    if HA > 0:
        A = 2 * np.pi - A
    return A

# LOOP---------------------------------------------------------
days=[]
altitude_list = []
azimuth_list = []

for i in range(1,int(T)+1):
    M = Mean_anomaly(i)
    #we are implicitely doing: true solar time = clock time + EOT and HA = 15º(true solar time-12h)
    H = np.radians((360/day) * -EOT(M, e, epsilon) / 60) 
    dec = delta(i)
    alt = altitude(H,dec)
    az = azimuth(dec, alt, H)
 
    altitude_list.append(np.degrees(alt))
    azimuth_list.append(np.degrees(az))
     

    

# PLOT-----------------------------------------------------

   
file_path = "C:/Users/Lenovo/Documents/assignment_astro/ephemeris_saturn.xlsx"  

excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(file_path, sheet_name="Sol")

az = df["az "].astype(float)
alt = df["alt"].astype(float)
plt.figure(figsize=(5, 9))
plt.scatter(azimuth_list, altitude_list, label='Simulated', s=3, color='pink')
plt.scatter(az, alt, label='Stellarium', s=2, color='blue')
plt.title(f"Analemma observed from (12:00h MST) 2025 - AGL")
plt.xlabel("Azimuth (°)")
plt.ylabel("Altitude (°)")
plt.legend()
plt.show()
