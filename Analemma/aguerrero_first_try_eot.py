
#STEP A: calculate Julian Date ot 0h UT with Year-Month-Date

# Date and hour in UT we want to compute the EOT
Y = 2025
M = 5
D = 16

UT = 12.0

if M>2:
    y = Y
    m = M - 3
else:
    y = Y-1
    m = M+9
    
JD = (np.floor(365.25 * (Y + 4712)) + np.floor(30.6*m + 0.5) +  D + 59 - 0.5

#STEP B: calculate the time arguments 't', the interval from 2000 January 1 at 12h UT
# to the date JD and time UT required in Julian centuries of 36525 d, and T the corresponding time interval in Dynamical Time:  
t = (JD + UT/24 - 2451545.0)/36525 #Julian centuries from J2000 using UT

deltat = np.floor(  −3.36 + 1.35(t + 2.33)**2 )* 10**(-8) #little correction

T = t + deltat #Julian centuries from J2000 using Ephemeris Time (ET)


#STEP C: calculate Greenwich mean sidereal time
ST = 100.4606 - 36000.77005 * t + 0.000388 * t**2 - 3*10**(-8)*t**3 #ST in degrees

#STEP D: calculate the right ascension of the apparent
  # STEP 1------------------ (MAGNITUDES IN DEGREES)
# L:  geometric mean ecliptic longitude of date
L = 280.46607 + 36000.76980 * T + 0.0003025 * T**2 

# G: Mean anomaly 
M = 357.528 + 35999.0503 * T 

# e: mean obliquity of the ecliptic
e = 23.4393- 0.01300* T + 0.0000002 * T**2 - 0.0000005 * T**3

# C: equation of center 
C = 
  # STEP 2-------------------------
#Ecliptic longitude of date = True solar longitude
L_dot = L + C -0.0057

  #STEP 3-----------------
#Right ascencion of the Sun
alpha = L_dot - np.tan(e/2)**2 * 180/np.pi * np.sin(2*L_dot) + 0.5 * (np.tan(e/2)**2)**2*180/np.pi*np.sin(4*L_dot)
