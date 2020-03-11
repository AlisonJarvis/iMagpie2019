#from pyorbital.astronomy import observer_position
from datetime import datetime
from datetime import timedelta
#from pyorbital import astronomy, dt2np
import math as math
import taskHelper
import numpy as np
#from pycraf import satellite
import matplotlib.pyplot as plt



utc_now = datetime.utcnow()

LAT = 40.010091
LONG = -105.243724
ALT = 1.623974#km

id = '25544'


AZ, EL, total_look_angular_rate, exposure_time = taskHelper.findtask(id,utc_now,LAT,LONG,ALT)

print('\n')
print('Azimuth (deg):')
print(AZ)
print('Elevation (deg):')
print(EL)
print('\n')

print('Rate of change of look angles (deg/s)')
print(total_look_angular_rate)
print('\n')

print('Calculated Exposure Time (Seconds):')
print(exposure_time)
print('\n')

"""
time_loop = datetime.utcnow()
time_temp = datetime.utcnow()
T = []
A1 = []
E1 = []
X1 = []
A2 = []
E2 = []
X2 = []
A3 = []
E3 = []
X3 = []
A1_rad = []
E1_rad = []
A2_rad = []
E2_rad = []
A3_rad = []
E3_rad = []

start_time = time_loop
start_hour = time_loop.hour
start_minute = time_loop.minute
start_second = time_loop.second
start_day = time_loop.day
while time_loop < time_temp + timedelta(hours=3):

    T = T + [(time_loop.minute - start_minute) + (time_loop.hour-start_hour)*60.0 + ((time_loop.second-start_second)/60.0) + (time_loop.day - start_day)*1440.0]
    temp_A, temp_E, temp_X = taskHelper.findtask(id,time_loop,LAT,LONG,ALT)
    A1 = A1 + [temp_A]
    A1_rad = A1_rad + [temp_A*(math.pi/180.0)]
    E1 = E1 + [temp_E]
    X1 = X1 + [temp_X]
    time_loop = time_loop + timedelta(seconds=1)

time_loop = start_time
id = '43058'

while time_loop < time_temp + timedelta(hours=3):

    temp_A, temp_E, temp_X = taskHelper.findtask(id,time_loop,LAT,LONG,ALT)
    A2 = A2 + [temp_A]
    A2_rad = A2_rad + [temp_A * (math.pi / 180.0)]
    E2 = E2 + [temp_E]
    X2 = X2 + [temp_X]
    time_loop = time_loop + timedelta(seconds=1)

time_loop = start_time
id = '37834'

while time_loop < time_temp + timedelta(hours=3):

    temp_A, temp_E, temp_X = taskHelper.findtask(id,time_loop,LAT,LONG,ALT)
    A3 = A3 + [temp_A]
    A3_rad = A3_rad + [temp_A * (math.pi / 180.0)]
    E3 = E3 + [temp_E]
    X3 = X3 + [temp_X]
    time_loop = time_loop + timedelta(seconds=1)

#fig, ax_list = plt.subplots(2,2)

fig = plt.figure()
ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(223)
ax4 = plt.subplot(224, projection='polar')

plt.suptitle('Propegation Results from {}/{}/{} {}:{} (UTC Time)'.format(start_time.month,start_time.day,start_time.year,start_time.hour,start_time.minute))

#Tnp = np.array(T)
#A1np = np.array(A1)
#A1_mask = np.ma.masked_where((A1np>355),A1np)
#A1_mask = np.ma.masked_where((A1np<5),A1np)
A1_mask = []
for i in range(0, len(A1)-1):
    if abs(A1[i]-A1[i+1]) < 355:
        A1_mask = A1_mask + [A1[i]]
    else:
        A1_mask = A1_mask + [np.ma.masked, np.ma.masked]
        i = i + 1
if len(A1_mask) - len(A1) == 1:
    del A1_mask[-1]
elif len(A1_mask) - len(A1) == -1:
    A1_mask = A1_mask + [A1[-1]]

A2_mask = []
for i in range(0, len(A2)-1):
    if abs(A2[i]-A2[i+1]) < 355:
        A2_mask = A2_mask + [A2[i]]
    else:
        A2_mask = A2_mask + [np.ma.masked, np.ma.masked]
        i = i + 1
if len(A2_mask) - len(A2) == 1:
    del A2_mask[-1]
elif len(A2_mask) - len(A2) == -1:
    A2_mask = A2_mask + [A2[-1]]

ax1.plot(T,A1_mask, label='ISS (LEO)')
ax1.plot(T,A2_mask, label='Galileo-22 (MEO)')
ax1.plot(T,A3, label='Intelsat-18 (GEO)')
ax1.set_title('Azimuth as a Function of Time')
ax1.set(ylabel='Degrees', xlabel='Minutes')
ax1.legend()


ax2.plot(T,E1, label='ISS (LEO)')
ax2.plot(T,E2, label='Galileo-22 (MEO)')
ax2.plot(T,E3, label='Intelsat-18 (GEO)')
ax2.plot([0,180],[20,20], label='Min for Viewing', linestyle='--')
ax2.set_title('Elevation as a Function of Time')
ax2.set(ylabel='Degrees', xlabel='Minutes')
ax2.legend()

ax3.plot(T,X1, label='ISS (LEO)')
ax3.plot(T,X2, label='Galileo-22 (MEO)')
ax3.plot(T,X3, label='Intelsat-18 (GEO)')
ax3.set_title('Angular Rate of Change of Look Angles as a Function of Time')
ax3.set(ylabel='Degrees per Second', xlabel='Minutes')
ax3.legend()

ax4.plot(A1_rad,E1, label='ISS (LEO)')
ax4.plot(A2_rad,E2, label='Galileo-22 (MEO)')
ax4.scatter(A3_rad,E3, label='Intelsat-18 (GEO)', linewidth=3, color='green')
ax4.set_title('Elevation as a Function of Azimuth')
ax4.set_ylabel('Elevation')
ax4.axis([0, 2*math.pi, 90, -90])
ax4.set_rticks([45, 0, -45, -90])
ax4.set_xticks([0, math.pi/4, 3.0*math.pi/4, 5.0*math.pi/4, 7.0*math.pi/4])
ax4.legend()

plt.show()

"""""

pre_AZ, pre_EL, pre_total_look_angular_rate, pre_exposure_time = taskHelper.findtask(id,utc_now - timedelta(seconds=exposure_time/2),LAT,LONG,ALT)
post_AZ, post_EL, post_total_look_angular_rate, post_exposure_time = taskHelper.findtask(id,utc_now + timedelta(seconds=exposure_time/2),LAT,LONG,ALT)


print("Azimuth (deg):")
print("Start: " + str(pre_AZ) + "   Mid: " + str(AZ) + "   End: " + str(post_AZ))
print("Elevation (deg):")
print("Start: " + str(pre_EL) + "   Mid: " + str(EL) + "   End: " + str(post_EL))
print("Predicted Length of Streak (deg):")
print(exposure_time*total_look_angular_rate)


