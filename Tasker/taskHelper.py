import math as math
import datetime
import numpy as np


# this function takes in lat, long and alt (km) of the observation site and converts it into ECEF position and velocity vectors

def site(lat, long, alt):
    lat = math.radians(lat)
    long = math.radians(long)

    sinLat = math.sin(lat)

    re = 6378.137
    flat = 1.0 / 298.257223563
    eccEarth = math.sqrt(2.0 * flat - flat ** 2)

    cEarth = re / math.sqrt(1.0 - ((eccEarth * sinLat) ** 2))

    rDel = (cEarth + alt) * math.cos(lat)
    rk = ((1.0 - eccEarth ** 2) * cEarth + alt) * sinLat

    rECEF = [rDel * math.cos(long), rDel * math.sin(long), rk]

    vECEF = [0.0, 0.0, 0.0]

    return [rECEF, vECEF]


def jday():
    time = datetime.datetime.utcnow()

    yr = time.year
    mon = time.month
    day = time.day
    min = time.minute
    hr = time.hour
    sec = time.second + time.microsecond * 10 ** (-6)

    jd = 367.0 * yr - math.floor((7 * (yr + math.floor((mon + 9) / 12.0))) * 0.25) + math.floor(275 * mon / 9.0) + day + 17201013.5

    js = (sec + min * 60.0 + hr * 3600.0) / 86400.0

    if js > 1.0:
        jd = jd + math.floor(js)
        js = js - math.floor(js)

    based = 367.0 * 1900 - math.floor((7 * (1900 + math.floor((1.0 + 9) / 12.0))) * 0.25) + math.floor(275 * 1.0 / 9.0) + 1.0 + 17201013.5

    bases = (12 * 3600.0) / 86400.0

    if bases > 1.0:
        based = based + math.floor(bases)
        bases = bases - math.floor(bases)

    jc = ((jd + js) - (based + bases)) / 36525.0

    return [jc, jd, js]


def gstime(jd):
    twopi = 2.0 * math.pi
    deg2rad = math.pi / 180.0

    tut1 = (jd - 2451545.0) / 36525.0

    temp = -6.2 * 10 ** (-6) * tut1 ** 3 + 0.093104 * tut1 ** 2 + (876600.0 * 3600.0 + 8640184.812866) * tut1 + 67310.54841

    temp = math.remainder(temp * deg2rad / 240.0, twopi)

    if temp < 0.0:
        temp = temp + twopi

    return temp


def polarm(xp, yp):

    cosxp = math.cos(xp)
    sinxp = math.sin(xp)
    cosyp = math.cos(yp)
    sinyp = math.sin(yp)

    pm = np.array([[cosxp, 0.0, -sinxp], [sinxp * sinyp, cosyp, cosxp * sinyp], [sinxp * cosyp, -sinyp, cosxp * cosyp]])

    return pm


def teme2ecef(Rteme, Vteme, jc, jd, js, xp, yp):

    deg2rad = math.pi / 180.0

    gmst = gstime(jd)

    omega = 125.04452222 + (-6962890.5390 * jc + 7.455 * jc ** 2 + 0.008 * jc ** 3) / 3600.0
    omega = math.remainder(omega, 360.0) * deg2rad

    gmstg = gmst + 0.00264 * math.pi / (3600.0 * 180.0) * math.sin(omega) + 0.000063 * math.pi / (3600.0 * 180.0) * math.sin(2.0 - omega)

    gmstg = math.remainder(gmstg, 2.0 * math.pi)

    st = np.array([[math.cos(gmstg), -math.sin(gmstg), 0.0], [math.sin(gmstg), math.cos(gmstg), 0.0], [0.0, 0.0, 1.0]])



    pm = np.array(polarm(xp, yp))



    Rpef = st.transpose().dot(Rteme)
    Recef = pm.transpose().dot(Rpef)


    thetasa = 7.29211514670698 * 10 ** (-5) * (1.0 * js / 86400.0)

    omegaearth = np.array([[0.0], [0.0], [thetasa]])

    Vpef = np.subtract(st.transpose().dot(Vteme),np.cross(omegaearth,Rpef,axis=0))
    Vecef = pm.transpose().dot(Vpef)

    return [Recef, Vecef]





def precess(jc):

    convrt = math.pi / (180.0*3600.0)
    jc2 = jc**2
    jc3 = jc**3

    psia = 5038.7784*jc - 1.07259*jc2 - 0.001147*jc3
    wa = 84381.448 + 0.05127*jc2 - 0.00726*jc3
    ea = 84381.448 - 46.8150*jc - 0.00059*jc2 + 0.001813*jc3
    xa = 10.5526*jc - 2.38064*jc2 - 0.001125*jc3
    zeta = 2306.2181*jc + 0.30188*jc2 + 0.017998*jc3
    theta = 2004.3109*jc - 0.42665*jc2 - 0.041833*jc3
    z = 2306.2181*jc + 1.09468*jc2 + 0.018203*jc3

    psia = psia * convrt
    wa = wa * convrt
    ea = ea * convrt
    xa = xa * convrt
    zeta = zeta * convrt
    theta = theta * convrt
    z = z * convrt

    coszeta = math.cos(zeta)
    sinzeta = math.sin(zeta)
    costheta = math.cos(theta)
    sintheta = math.sin(theta)
    cosz = math.cos(z)
    sinz = math.sin(z)

    prec = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

    prec[0][0] = coszeta*costheta*cosz-sinzeta*sinz
    prec[0][1] = coszeta*costheta*sinz+sinzeta*cosz
    prec[0][2] = coszeta*sintheta
    prec[1][0] = -sinzeta*costheta*cosz-coszeta*sinz
    prec[1][1] = -sinzeta*costheta*sinz+coszeta*cosz
    prec[1][2] = -sinzeta*sintheta
    prec[2][0] = -sintheta*cosz
    prec[2][1] = -sintheta*sinz
    prec[2][2] = costheta

    return [prec, psia, wa, ea, xa]


def nutation(jc, ddpsi, ddeps):

    deg2rad = math.pi/180.0

    convrt = 0.0001 * math.pi / (180*3600.0)

    nut80 = np.genfromtxt("nut80.dat")

    iar80 = nut80[:][0:4]
    rar80 = nut80[:][5:8]

    for i in range(106):
        for j in range(4):
            rar80[i][j] = rar80[i][j]*convrt

    jc2 = jc**2
    jc3 = jc**3

    meaneps = -46.8150 * jc - 0.00059 * jc2 + 0.001813 * jc3 + 84381.448
    meaneps = math.remainder(meaneps/3600.0, 360.0)
    meaneps = meaneps * deg2rad

    [l, ll, f, d, omega, lonmer, lonven, lonear, lonmar, lonjup, lonsat, lonurn, lonnep, precrate] = fundarg(jc)

    deltapsi = 0.0
    deltaeps = 0.0

    for i in range(107,0,-1):
        tempval = iar80[i][0]*l + iar80[i][1]*ll + iar80[i][2]*f + iar80[i][3]*d + iar80[i][4]*omega
        deltapsi = deltapsi + (rar80[i][0] + rar80[i][1]*jc)*math.sin(tempval)
        deltaeps = deltaeps + (rar80[i][2] + rar80[i][3]*jc)*math.cos(tempval)

    deltapsi = math.remainder(deltapsi + ddpsi, 2.0*math.pi)
    deltaeps = math.remainder(deltaeps + ddeps, 2.0*math.pi)
    trueeps = meaneps + deltaeps

    cospsi = math.cos(deltapsi)
    sinpsi = math.sin(deltapsi)
    coseps = math.cos(meaneps)
    sineps = math.sin(meaneps)
    costrueeps = math.cos(trueeps)
    sintrueeps = math.sin(trueeps)

    nut = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

    nut[0][0] = cospsi
    nut[0][1] = costrueeps * sinpsi
    nut[0][2] = sintrueeps * sinpsi
    nut[1][0] = -coseps * sinpsi
    nut[1][1] = costrueeps * coseps * cospsi + sintrueeps * sineps
    nut[1][2] = sintrueeps * coseps * cospsi - sineps * costrueeps
    nut[2][0] = -sineps * sinpsi
    nut[2][1] = costrueeps * sineps * cospsi - sintrueeps * coseps
    nut[2][2] = sintrueeps * sineps * cospsi + costrueeps * coseps

    return [deltapsi, trueeps, meaneps, omega, nut]


def fundarg(jc):

    deg2rad = math.pi/180.0

    l = ((((0.064) * jc + 31.310) * jc + 1717915922.6330) * jc) / 3600.0 + 134.96298139
    ll = ((((-0.012) * jc - 0.577) * jc + 129596581.2240) * jc) / 3600.0 + 357.52772333
    f = ((((0.011) * jc - 13.257) * jc + 1739527263.1370) * jc) / 3600.0 + 93.27191028
    d = ((((0.019) * jc - 6.891) * jc + 1602961601.3280) * jc) / 3600.0 + 297.85036306
    omega = ((((0.008) * jc + 7.455) * jc - 6962890.5390) * jc) / 3600.0 + 125.04452222

    lonmer = 252.3 + 149472.0 * jc
    lonven = 179.9 + 58517.8 * jc
    lonear = 98.4 + 35999.4 * jc
    lonmar = 353.3 + 19140.3 * jc
    lonjup = 32.3 + 3034.9 * jc
    lonsat = 48.0 + 1222.1 * jc
    lonurn = 0.0
    lonnep = 0.0
    precrate = 0.0

    l = math.remainder(l, 360.0) * deg2rad
    ll = math.remainder(ll, 360.0) * deg2rad
    f = math.remainder(f, 360.0) * deg2rad
    d = math.remainder(d, 360.0) * deg2rad
    omega = math.remainder(omega, 360.0) * deg2rad

    lonmer = math.remainder(lonmer, 360.0) * deg2rad
    lonven = math.remainder(lonven, 360.0) * deg2rad
    lonear = math.remainder(lonear, 360.0) * deg2rad
    lonmar = math.remainder(lonmar, 360.0) * deg2rad
    lonjup = math.remainder(lonjup, 360.0) * deg2rad
    lonsat = math.remainder(lonsat, 360.0) * deg2rad
    lonurn = math.remainder(lonurn, 360.0) * deg2rad
    lonnep = math.remainder(lonnep, 360.0) * deg2rad
    precrate = math.remainder(precrate, 360.0) * deg2rad

    return [l, ll, f, d, omega, lonmer, lonven, lonear, lonmar, lonjup, lonsat, lonurn, lonnep, precrate]


def rot2(vec, xval):

    temp = vec[2]
    c = math.cos(xval)
    s = math.sin(xval)

    outvec = np.array([[0.0],[0.0],[0.0]])

    outvec[2] = c*vec[2] + s*vec[0]
    outvec[0] = c*vec[0] - s*temp
    outvec[1] = vec[1]

    return [outvec]


def rot3(vec, xval):

    temp = vec[1]

    c = math.cos(xval)
    s = math.sin(xval)

    outvec = np.array([[0.0],[0.0],[0.0]])

    outvec[1] = c*vec[1] - s*vec[0]
    outvec[0] = c*vec[0] + s*temp
    outvec[2] = vec[2]
    return [outvec]





def sidereal(jdut1, deltapsi, meaneps, omega, lod, eqeterms):
    gmst = gstime(jdut1)
    if (jdut1 > 2450449.5) and (eqeterms>0):
        ast = gmst + deltapsi * math.cos(meaneps) + 0.00264*math.pi /(3600*180)*math.sin(omega) + 0.000063*math.pi /(3600*180)*math.sin(2.0 *omega)
    else:
        ast = gmst + deltapsi * math.cos(meaneps)

    ast = math.remainder(ast, 2.0 * math.pi)
    thetasa = 7.29211514670698e-05 * (1.0 - lod / 86400.0)
    omegaearth = thetasa

    st = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    st[0][0] = math.cos(ast)
    st[0][1] = -math.sin(ast)
    st[0][2] = 0.0
    st[1][0] = math.sin(ast)
    st[1][1] = math.cos(ast)
    st[1][2] = 0.0
    st[2][0] = 0.0
    st[2][1] = 0.0
    st[2][2] = 1.0

    stdot = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    stdot[0][0] = -omegaearth * math.sin(ast)
    stdot[0][1] = -omegaearth * math.cos(ast)
    stdot[0][2] = 0.0
    stdot[1][0] = omegaearth * math.cos(ast)
    stdot[1][1] = -omegaearth * math.sin(ast)
    stdot[1][2] = 0.0
    stdot[2][0] = 0.0
    stdot[2][1] = 0.0
    stdot[2][2] = 0.0

    return [st,stdot]


def ECEF2AZEL(R_sat_ECEF,V_sat_ECEF,R_site_ECEF,V_site_ECEF,lat,lon):

    halfpi = math.pi*0.5
    small = 0.00000001
    rhoecef = R_sat_ECEF - R_site_ECEF
    drhoecef = V_sat_ECEF
    rho = np.sqrt(rhoecef.transpose().dot(rhoecef))

    [tempvec] = rot3(rhoecef, lon)
    [rhosez] = rot2(tempvec, halfpi-lat)

    [tempvec] = rot3(drhoecef, lon)
    [drhosez] = rot2(tempvec, halfpi-lat)
    temp = math.sqrt(rhosez[0]**2 + rhosez[1]**2)

    if temp < small:
        el = np.sign(rhosez[2])*halfpi
        az = math.atan2(drhosez[1],-drhosez[0])
    else:
        magrhosez = np.sqrt(rhosez.transpose().dot(rhosez))
        el = math.asin(rhosez[2]/magrhosez)
        az = math.atan2(rhosez[1]/temp,-rhosez[0]/temp)

    drho = np.dot(rhosez.transpose(),drhosez)/rho

    if abs(temp**2) > small:
        daz = (drhosez[0]*rhosez[1] - drhosez[1]*rhosez[0])/(temp**2)
    else:
        daz = 0.0

    if abs(temp) > small:
        DEL = (drhosez[2]-drho*math.sin(el))/temp
    else:
        DEL = 0.0

    return [rho, az, el, drho, daz, DEL]

## unused
#
#
#
#
#
#
#
#
#
#
3
3
3
3
#


def teme2eci(Rteme, Vteme, jc, ddpsi, ddeps):

    [prec, psia, wa, ea, xa] = precess(jc)
    [deltapsi, trueeps, meaneps, omega, nut] = nutation(jc, ddpsi, ddeps)

    eqeg = deltapsi*math.cos(meaneps)
    eqeg = math.remainder(eqeg, 2.0*math.pi)

    eqe = np.array([[math.cos(eqeg), math.sin(eqeg), 0.0], [-math.sin(eqeg), math.cos(eqeg), 0.0], [0.0, 0.0, 1.0]])

    tm = prec * nut * eqe.transpose()

    Reci = tm.dot(Rteme)
    Veci = tm.dot(Vteme)

    return [Reci, Veci]

def ecef2eci(recef,vecef,aecef,ttt,jdut1,lod,xp,yp,eqeterms,ddpsi,ddeps):

    [prec, psia, wa, ea, xa] = precess(ttt)

    [deltapsi, trueeps, meaneps, omega, nut] = nutation(ttt, ddpsi, ddeps)

    [st, stdot] = sidereal(jdut1, deltapsi, meaneps, omega, lod, eqeterms)

    [pm] = polarm(xp,yp)

    thetasa = 7.29211514670698e-05 * (1.0 - lod / 86400.0)
    omegaearth = np.array([0.0,0.0,thetasa])

    rpef = pm.dot(recef)
    reci = prec.dot(nut).dot(st).dot(rpef)
    vpef = pm.dot(vecef)
    veci = (prec.dot(nut).dot(st).dot(np.add(vpef, np.cross(omegaearth,rpef))))

    temp = np.cross(omegaearth,rpef)
    aeci = prec.dot(nut).dot(st).dot(np.add(np.add(pm.dot(aecef),np.cross(omegaearth,temp)),np.multiply(2.0,np.cross(omegaearth,vpef))))

    return [reci, veci, aeci]