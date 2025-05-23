# -*- coding: utf-8 -*-
"""
Created on Sun May 18 19:35:24 2025

@author: andrea
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# SIMULATION OF SOLAR ANALEMMA FROM EARTH AT NOON 
# DATA INPUTS------------------------------------------------

# Parameters of Earth's orbit
e=0.0176
epsilon=np.radians(23.45)
P = np.radians(12.9)
T=365.25

#Coordenates Bellaterra
phi = np.radians(41.505789)
landa = np.radians(2.089509)

# EQUATIONS--------------------------------------------------
def Mean_anomaly(N): # Mean anomaly for day N
    return 2*np.pi*(N-3)/T

def EOT(Ma, ecc, tilt):  # Equation Of Time in minutes
    return -( -2*ecc*np.sin(Ma)-(np.tan(tilt/2))**2 * np.sin(2*(Ma+P)) ) * (720 / np.pi) 
 #in minutes

def delta(N): #Sun's declination
    return -epsilon * np.cos((2*np.pi*(N+10))/T)

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

for i in range(1,366):
    M = Mean_anomaly(i)
    #we are implicitely doing: true solar time = clock time + EOT and HA = 15º(true solar time-12h)
    H = np.radians(15 * -EOT(M, e, epsilon) / 60) 
    dec = delta(i)
    alt = altitude(H,dec)
    az = azimuth(dec, alt, H)
 
    altitude_list.append(np.degrees(alt))
    azimuth_list.append(np.degrees(az))
    

# COMPARISON WITH STELLARIUM DATA
    
file_path = "C:/Users/Lenovo/Documents/assignment_astro/ephemeris.xlsx"  

excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(file_path, sheet_name="Sol")

az = df["az Earth"].astype(float)
alt = df["alt Earth"].astype(float)
    

# PLOT-----------------------------------------------------
plt.figure(figsize=(5, 9))
plt.scatter(azimuth_list, altitude_list, label='Simulated', s=3, color='pink')
plt.scatter(az, alt, label='Stellarium', s=2, color='blue')
plt.title("Analemma observed from Bellaterra (12:00h) 2025 - AGL")
plt.xlabel("Azimuth (°)")
plt.ylabel("Altitude (°)")
plt.legend()
plt.show()
    

