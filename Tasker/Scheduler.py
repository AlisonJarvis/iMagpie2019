from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import datetime
import math as math
import taskHelper
import sgp4 as sgp4
import numpy as np
from pycraf import satellite


## Some constants i think

xp = 0.1206
yp = 0.3449


##time stuff happens here

time = datetime.datetime.utcnow()

jc, jd, js = taskHelper.jday()


##Site stuff happens here

LAT = 40.010091
LONG = -105.243724
ALT = 1.623974#km

R_site_ECEF, V_site_ECEF = taskHelper.site(LAT,LONG,ALT)

#R_site_ECEF = np.array([[R_site_ECEF[0]],[R_site_ECEF[1]],[R_site_ECEF[2]]])
#V_site_ECEF = np.array([[V_site_ECEF[0]],[V_site_ECEF[1]],V_site_ECEF[2]])

## select satellite and propegate

id = '43873'
id = id.rjust(5)

counter = 0

with open ('3le.txt', 'r') as TLEs:
    for line in TLEs:
        if line[2:7] == id and counter == 0:
            #print(line)
            line1 = line
            counter = 1
        elif line[2:7] == id and counter == 1:
            line2 = line
            #print(line)
            break



satellite = twoline2rv(line1,line2,wgs72)

R_sat_TEME, V_sat_TEME = satellite.propagate(time.year,time.month,time.day,time.hour,time.minute,(time.second + time.microsecond*10**(-6)))

R_sat_TEME = np.array([[R_sat_TEME[0]],[R_sat_TEME[1]],[R_sat_TEME[2]]])
V_sat_TEME = np.array([[V_sat_TEME[0]],[V_sat_TEME[1]],[V_sat_TEME[2]]])


R_sat_ECEF, V_sat_ECEF = taskHelper.teme2ecef(R_sat_TEME,V_sat_TEME,jc,jd,js, xp, yp)

print('\nSat ECEF X Y Z:')
print(R_sat_ECEF)
print(np.sqrt(R_sat_ECEF.transpose().dot(R_sat_ECEF))-6371)

[rho, az, el, drho, daz, DEL] = taskHelper.ECEF2AZEL(R_sat_ECEF,V_sat_ECEF,R_site_ECEF,V_site_ECEF,LAT,LONG)




##convert rad to deg

rad2deg = 180.0/math.pi

az = az*rad2deg
el = el*rad2deg
daz = daz*rad2deg
DEL = DEL*rad2deg


print('\nAzimuth & Elevation:')
print(az)
print(el)
print('\nDaz and Del:')
print(daz)
print(DEL)

#print(Recef_sat)

#print(np.sqrt(Recef_sat.dot(Recef_sat)))
#print(np.sqrt(Vecef_sat.dot(Vecef_sat)) * 3600)
#relativePOS = Recef_sat - Recef_site
#relativeVEL = Vecef_sat - Vecef_site

#print(relativePOS)
#print(relativeVEL)


