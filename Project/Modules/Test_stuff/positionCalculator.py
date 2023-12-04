import math
import spiceypy
import os
import sys

def main():
    leapseconds_kernel = "naif0012.tls"
    leapseconds_kernel_path = getFilePath(leapseconds_kernel )
    os.chdir(os.path.dirname(leapseconds_kernel_path))
    print("Version:" + spiceypy.tkvrsn("Toolkit"))
    spiceypy.furnsh(leapseconds_kernel)
    print("Kernels loaded!")
    # Sun and Earth orbit type is elliptical,that means it's eccentricity = (0-1)
    
    print("Earth eccentrity in j2000")
    earth_eccentricity = 0.016709
    
    # Obliquity of ecliptic {degrees} (oblecl)
    earth_obliquity_of_ecliptic = 23.4393

    # Semi-major axis or Mean distance (a)
    semi_major_axis = 0
    mean_distance = semi_major_axis
    sun_mean_distance = 1.000000 #in AU (Astronomical Units)

    # Angle from the Ascending node to the Perihelion, along the orbit {degrees} (w)
    sun_longtitude_of_perihelion = 282.9404

    # longitude of Ascending Node (N),{degrees}
    ascending_node_longtitude = 0

    # Inclination (i) {degrees 0-180}
    sun_inclination = 0

    # Perihellion distance (q)
    perihellion_distance = 0
    # Formula for perihellion distance is: a * (1 - e),[a = semi-major or mean distance axis, e = eccentricity]

    # Aphelion distance (Q)
    aphelion_distance = 0
    # Formula for aphelion distance is: a * (1 + e),[a = semi-major or mean distance axis, e = eccentricity]

    # Time at perihellion in UTC format YYYY DD MM HH:MM:SS (T)
    time_at_perihellion = "1999 31 Dec 00:00:00"

    # Time in UTC format YYYY DD MM HH:MM:SS (t)
    time = "1990 19 Apr 00:00:00"

    # Orbital period (P)
    sun_orbital_period = 365.256898326 * sun_mean_distance**1.5/math.sqrt(1)
    # Formula for Orbital period is: 365.256898326(Days in 1 year) * a**1.5/sqrt(1+m){Days} ,[a = semi-majsemi-major or mean distance axis,m = mass of the planet in solar masses]

    # Daily motion (n)
    # sun_daily_motion = 360/sun_orbital_period
    sun_daily_motion = 0.9856002585
    print("sun daily motion {}".format(sun_daily_motion))
    # Formula for daily motion is: 360(deg)/ P {degrees/day}

    # time(t) - Time at perihellion(T)
    delta_time = spiceypy.str2et(time) - spiceypy.str2et(time_at_perihellion)

    # Day number (d)
    day_number = delta_time/86400
    # To get day_number use: spiceypy.str2et(delta_time)/86400

    # Mean Anomaly (M)
    sun_mean_anomaly = 356.0470 + sun_daily_motion * day_number
    #Formula for Mean Anomaly is: n * (delta_time{days}), [n = Daily notion]

    # Mean longitude (L)
    sun_mean_longtitude = 0
    #Formula for Mean longitude is: M + w + N, [M = Mean anomaly, w = small_omega, N = longitude of Ascending Node]

    # Eccentric anomaly (E)
    eccentric_anomaly = 0
    # Formula for Eccentric anomaly, is defined by Kepler's equation: M = E - e*sin(E)

    # True anomaly "The angle from perihelion to the planet, as seen from the Sun" (v)
    true_anomaly = 0

    # Heliocentric distance "The planet's distance from the Sun" (r)
    helio_distance = 0

    # Relation that valid for an elliptic orbit

    # r * cos(v) = a * (cos(E) - e)
    # r * sin(v) = a * sqrt(1 - e*e) * sin(E)
    # [r = Heliocentric distance, v = True anomaly, E = Eccentric anomaly, e = Eccentricity ]

    # Rectangular coordinates (x,y,z)
    x = 0
    y = 0
    z = 0
    rectangular_coordinates = (x,y,z)

    # Formulas to convert spheriacal coordinates to rectangular coordinates

    # x = r * cos(RA) * cos(Decl),
    # y = r * sin(RA) * cos(Decl)
    # z = r * sin(Decl)
    ## [RA = Right Ascension, Decl = Declination]

    

    find_sun_pos(day_number,sun_longtitude_of_perihelion,sun_mean_distance, sun_mean_anomaly, earth_eccentricity,earth_obliquity_of_ecliptic,helio_distance,true_anomaly)
    spiceypy.kclear()

    print("Kernels unloaded!")

def find_sun_pos(day_number,sun_longtitude_of_perihelion,sun_mean_distance,sun_mean_anomaly,earth_eccentricity,earth_obliquity_of_ecliptic,helio_distance,true_anomaly):
    d = day_number
    print("Days after or before J2000: {}".format(d))
    w = sun_longtitude_of_perihelion + 4.70935E-5 * d                   # longitude of perihelion
    print("longitude of perihelion: {}°".format(w))               
    a = sun_mean_distance                                               # Mean distance in AU
    print("Mean distance(AU): {}".format(a))               
    mM = sun_mean_anomaly                                               # Mean Anomaly
    if mM <0:               
        mM = rev(mM)               
    print("Mean anomaly: {}°".format(mM))               
    e = earth_eccentricity - 1.151E-9 * d                               # Eccentricity
    (print("Eccentricity: {}".format(e)))
    oblecl = earth_obliquity_of_ecliptic - 3.563E-7 * d                 # Obliquity of the ecliptic
    print("Obliquity of the ecliptic: {}°".format(oblecl))
    mL = w + mM                                                         # Mean longitude
    if mL>360:
        mL = rev(mL)
    print("Mean longitude: {}°".format(mL))
    print(math.sin(mM))
    mE = mM + (180/math.pi) * e * sind(mM) * (1 + e * cosd(mM)) # Eccentric anomaly
    print("Eccentric anomaly: {}°".format(mE))
    x = cosd(mE) - e
    print("X-EclipticCoordinate: {}".format(au2km(x)))          # X ECLIPTIC FRAME 
    y = sind(mE) * math.sqrt(1 - e*e)
    print("Y-EclipticCoordinate: {}".format(au2km(y)))          # Y ECLIPTIC FRAME
    z = 0
    print("Z-EclipticCoordinate: {}".format(au2km(z)))          # Z ECLIPTIC FRAME
    r = helio_distance = math.sqrt(x*x +y*y)                    # Heliocentric distance
    print("Helliocentric distance: {}".format(r))
    v = atand2(y,x)                                             # True anomaly
    print("True anomaly: {}".format(v))
    sun_longitude = v + w                                       # Sun longitude
    if sun_longitude > 360:
        sun_longitude = rev(sun_longitude)
    print("Sun longitude: {}".format(sun_longitude))
    xequat = r * cosd(sun_longitude)
    yequat = r * sind(sun_longitude)
    zequat = 0.0
    zequat = yequat * sind(oblecl) + 0.0 * cosd(oblecl)
    yequat = yequat * cosd(oblecl) + 0.0 * cosd(oblecl)
    print("X-EqutorialCoordinate(AU): {}".format(xequat))           # X EQUATORIAL FRAME
    print("Y-EqutorialCoordinate(AU): {}".format(yequat))           # Y EQUATORIAL FRAME
    print("Z-EqutorialCoordinate(AU): {}".format(zequat))           # Z EQUATORIAL FRAME
    print("X-EqutorialCoordinate(KM): {}".format(au2km(xequat)))           
    print("Y-EqutorialCoordinate(KM): {}".format(au2km(yequat)))           
    print("Z-EqutorialCoordinate(KM): {}".format(au2km(zequat))) 
    
def getFilePath(fileName):
    rootDirectory = os.getcwd()
    for relativePath,dirs,files in os.walk(rootDirectory):
        if(fileName in files):
            filePath = os.path.join(rootDirectory,relativePath,fileName)
            return(filePath)
    print("Error occured:")
    sys.exit("File " + fileName + " not found")

def rev(x):
    return x - x//360*360
def sind(x):
    return math.sin(math.radians(x))
def cosd(x):
    return math.cos(math.radians(x))
def au2km(x):
    return x*1.496e+8
def atand2(x,y):
    return math.degrees(math.atan2(x,y))

if __name__ == "__main__":
    main()