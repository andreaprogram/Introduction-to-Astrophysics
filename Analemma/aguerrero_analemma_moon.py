# -*- coding: utf-8 -*-
"""
Created on Thu May 22 22:43:36 2025

@author: Lenovo
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# SIMULATION OF AN ANALEMMA
# DATA INPUTS------------------------------------------------

# Parameters of Moon's orbit
e=0.0549
epsilon=np.radians(6.68)
P = np.radians(200)
T=28 #days
day = 708.7	 #hours

#Coordenates Bellaterra
phi = np.radians(41.505789)
landa = np.radians(2.089509)

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
    t = 18 - EOT(M, e, epsilon) / 60 #hours
    H = np.radians((360/day) * (t -12)) 
    dec = delta(i)
    alt = altitude(H,dec)
    az = azimuth(dec, alt, H)
 
    altitude_list.append(np.degrees(alt))
    azimuth_list.append(np.degrees(az))
     

    

file_path = "C:/Users/Lenovo/Documents/assignment_astro/ephemeris_moon.xlsx"  

excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(file_path, sheet_name="Luna")

az = df["az"].astype(float)
alt = df["alt"].astype(float)
#plt.figure(figsize=(5, 9))
plt.scatter(azimuth_list, altitude_list, label='Simulated', s=3, color='pink')
#plt.plot(az, alt, label='Stellarium', color='blue')
plt.title(f"Analemma observed from (12:00h MST) 2025 - AGL")
plt.xlabel("Azimuth (°)")
plt.ylabel("Altitude (°)")
plt.legend()
plt.show()