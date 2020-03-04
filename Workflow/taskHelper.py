from pyorbital.astronomy import observer_position
from pyorbital import astronomy, dt2np
import math as math
import numpy as np
from pycraf import satellite


def logical_cross(A, B):

    i = A[1]*B[2] - B[1]*A[2]
    j = -(A[0]*B[2]-B[0]*A[2])
    k = A[0]*B[1] - B[0]*A[1]

    result = np.array([i, j, k])

    return result


def findtask(norad_id, observation_time, LAT, LONG, ALT):

    id = norad_id
    id = id.rjust(5)

    counter = 0

    with open('3le.txt', 'r') as TLEs:
        for line in TLEs:
            if line[2:7] == id and counter == 0:
                # print(line)
                line1 = line
                counter = 1
            elif line[2:7] == id and counter == 1:
                line2 = line
                # print(line)
                break

    R_site_ECI, V_site_ECI = observer_position(observation_time, LONG, LAT, ALT)

    sat = satellite.get_sat(line1, line2)

    R_sat_ECI, V_sat_ECI = sat.propagate(observation_time.year, observation_time.month, observation_time.day, observation_time.hour, observation_time.minute,
                                         (observation_time.second + observation_time.microsecond * 10 ** (-6)))

    delta_R = np.array([[R_sat_ECI[0] - R_site_ECI[0]], [R_sat_ECI[1] - R_site_ECI[1]], [R_sat_ECI[2] - R_site_ECI[2]]])
    delta_V = np.array([[V_sat_ECI[0] - V_site_ECI[0]], [V_sat_ECI[1] - V_site_ECI[1]], [V_sat_ECI[2] - V_site_ECI[2]]])

    utc_time = dt2np(observation_time)

    lon = np.deg2rad(LONG)
    lat = np.deg2rad(LAT)

    theta = (astronomy.gmst(utc_time) + lon) % (2 * np.pi)

    sin_lat = np.sin(lat)
    cos_lat = np.cos(lat)
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    top_s = sin_lat * cos_theta * delta_R[0] + \
            sin_lat * sin_theta * delta_R[1] - cos_lat * delta_R[2]
    top_e = -sin_theta * delta_R[0] + cos_theta * delta_R[1]
    top_z = cos_lat * cos_theta * delta_R[0] + \
            cos_lat * sin_theta * delta_R[1] + sin_lat * delta_R[2]

    az_ = np.arctan(-top_e / top_s)

    az_ = np.where(top_s > 0, az_ + np.pi, az_)
    az_ = np.where(az_ < 0, az_ + 2 * np.pi, az_)

    rg_ = np.sqrt(top_s * top_s + top_e * top_e + top_z * top_z)

    el_ = np.arcsin(top_z / rg_)

    AZ = np.rad2deg(az_)
    EL = np.rad2deg(el_)

    mag_delta_R = math.sqrt(delta_R[0] ** 2 + delta_R[1] ** 2 + delta_R[2] ** 2)
    unit_delta_R = np.array([delta_R[0] / mag_delta_R, delta_R[1] / mag_delta_R, delta_R[2] / mag_delta_R])

    V_orth_R_ECI = logical_cross(logical_cross(unit_delta_R, delta_V), unit_delta_R)

    total_look_angular_rate = (math.sqrt(V_orth_R_ECI[0] ** 2 + V_orth_R_ECI[1] ** 2 + V_orth_R_ECI[2] ** 2) / \
                               math.sqrt(delta_R[0] ** 2 + delta_R[1] ** 2 + delta_R[2] ** 2)) * (180.0 / math.pi)

    exposure_time = 0.955/total_look_angular_rate

    if exposure_time > 10:
        exposure_time = 10

    return [AZ[0], EL[0], total_look_angular_rate, exposure_time]