# -*- coding: utf-8 -*-
"""
Created on Tue May 13 18:09:33 2025

@author: Lenovo
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Plot of the EOT
e=0.0176
epsilon=np.radians(23.45)
P = np.radians(12.3)
T=365.25

#Compute Mean anomaly for day N
def M(N):
    return 2*np.pi*(N-3)/T

def EOT(Ma, ecc, tilt):
    return -( -2*ecc*np.sin(Ma)-(np.tan(tilt*0.5))**2 * np.sin(2*(Ma+P)) ) * (720 / np.pi)
 #in minutes
    
EOT_l=[]
EOT_circ=[] 
EOT_tiltless=[]
days=[]

for i in range(1,366):
    days.append(i)
    EOT_l.append(EOT(M(i),e,epsilon))
    EOT_circ.append(EOT(M(i),0,epsilon))
    EOT_tiltless.append(EOT(M(i),e,0))

plt.figure(figsize=(10, 4))
plt.plot(days, EOT_l, color='black', label=r'$e=0,0176$  $\epsilon=23,45°$')
plt.plot(days, EOT_circ, color='violet',  linestyle='--', label=r'$e=0$  $\epsilon=23,45°$')
plt.plot(days, EOT_tiltless, color='pink', linestyle='--',  label=r'$e=0,0176$  $\epsilon=0$')
plt.title("Equation of Time 2025 - AGL")
plt.xlabel("Day of the year")
plt.ylabel("EOT (min)")
plt.legend()
plt.show()