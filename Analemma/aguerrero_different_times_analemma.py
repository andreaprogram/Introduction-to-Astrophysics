# -*- coding: utf-8 -*-
"""
Created on Mon May 19 00:16:21 2025

@author: andrea
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# SIMULATION OF AN ANALEMMA
# DATA INPUTS------------------------------------------------

# Parameters of Earth's orbit
e=0.0176
epsilon=np.radians(23.45)
P = np.radians(12.3)
T=365.25

#Coordenades Bellaterra
phi = np.radians(41.505789)
landa = np.radians(2.089509)

# EQUATIONS--------------------------------------------------
def Mean_anomaly(N): # Mean anomaly for day N
    return 2*np.pi*(N-3)/T

def EOT(Ma, ecc, tilt): #Equation Of Time)
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
times = [10, 11, 12, 13, 14]  # in hours
colors = ['red', 'orange', 'green', 'blue', 'purple']
j=0

for t in times:
    days=[]
    altitude_list = []
    azimuth_list = []
    
    for i in range(1,366):
        M = Mean_anomaly(i)
        solar_time = t + (EOT(M,e,epsilon))/60
        H = np.radians(15 * (solar_time - 12))
        dec = delta(i)
        alt = altitude(H,dec)
        az = azimuth(dec, alt, H)
     
        altitude_list.append(np.degrees(alt))
        azimuth_list.append(np.degrees(az))
        
    plt.plot(azimuth_list, altitude_list, linewidth=1, label=t, color=colors[j])
    j+=1
    
# PLOT-----------------------------------------------------
plt.title("Analemmas observed from Bellaterra at different clock times 2025 - AGL")
plt.xlabel("Azimuth (°)")
plt.ylabel("Altitude (°)")
plt.legend()
plt.show()