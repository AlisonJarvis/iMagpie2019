import serial
import time


class Mount:

    alt = 0
    az = 0
    ra = 0
    dec = 0
    altaz = True

    def __init__(self, port, baud, time_out):
        self.ser = serial.Serial(port, baud, timeout=time_out)

    def decode_alt_az(self, inputstr):
        alt = inputstr[0] + str(int(inputstr[1:9]) / 360000)
        az = str(int(inputstr[10:18]) / 360000)
        return [alt, az]

    def current_alt_az(self):
        self.ser.write(b':GAC#')
        response = self.ser.readline()
        packet = response.decode()
        return self.decode_alt_az(packet)

    def set_alt_limit(self, limit):
        self.ser.write(b':SAL'+limit.encode()+b'#')
        response = self.ser.readline()
        packet = response.decode()
        if packet != "1":
            print("Error: Limit set command denied")

        return packet

    def current_alt_limit(self):
        self.ser.write(b':GAL#')  # check altitude limit
        response = self.ser.readline()
        packet = response.decode()
        return packet

    def set_track_type(self, t_type):
        self.ser.write(b':RT' + t_type.encode() + b'#')
        response = self.ser.readline()
        packet = response.decode()
        if packet != "1":
            print("Error: Track type not valid or something\n0: sidereal  2: solar")

        return packet

    def set_time_zone(self, offset_from_utc):
        #for mst -420
        self.ser.write(b'SG' + offset_from_utc.encode())
        response = self.ser.readline()
        packet = response.decode()
        if packet != "1":
            print("Error: invalid input")

        return packet

    def set_daylight_savings(self, dst):
        #0 or 1
        self.ser.write(b':SDS'+dst.encode()+b'#')
        response = self.ser.readline()
        packet = response.decode()
        if packet != "1":
            print("Error: invalid input")

        return packet

    def set_alt_az(self, alt, az):

        self.altaz = True

        alt = alt * 360000
        alt = round(alt)
        self.alt = alt
        if alt >= 0:
            signstr = '+'
        else:
            signstr = '-'
        alt = abs(alt)
        alt = str(alt)
        alt = alt.rjust(8, '0')

        az = az * 360000
        az = round(az)
        self.az = az
        az = str(az)
        az = az.rjust(8, '0')

        self.ser.write(b':Sa' + signstr.encode() + alt.encode() + b'#')  # define command altitude
        response1 = self.ser.readline()
        packet1 = response1.decode()
        if packet1 != "1":
            print("Error: Alt command denied")

        self.ser.write(b':Sz' + az.encode() + b'#')  # define command azimuth
        response2 = self.ser.readline()
        packet2 = response2.decode()
        if packet2 != "1":
            print("Error: Az command denied")

        return [packet1, packet2]

    def slew_to_coordinates(self):
        self.ser.write(b':MS#')  # command to slew to defined coordinates
        response = self.ser.readline()
        packet = response.decode()
        if packet != "1":
            print("Error: Slew command denied")
            return packet
        else:
            if self.altaz:
                packet_check = self.current_alt_az()
                alt = int(packet_check[0:8])
                az = int(packet_check[9:17])
                while (alt<(self.alt-10)) or (alt>(self.alt+10)) or (az<(self.az-10)) or (az>(self.az+10)):
                    packet_check = self.current_alt_az()
                    alt = int(packet_check[0:8])
                    az = int(packet_check[9:17])
                    time.sleep(0.5)
                return packet
            else:
                packet_check = self.current_ra_dec()
                dec = int(packet_check[0:8])
                ra = int(packet_check[9:16])
                while (ra<(self.alt-10)) or (ra>(self.alt+10)) or (dec<(self.az-10)) or (dec>(self.az+10)):
                    packet_check = self.current_alt_az()
                    dec = int(packet_check[0:8])
                    ra = int(packet_check[9:16])
                    time.sleep(0.5)
                return packet

    def start_stop_tracking(self, command):
        self.ser.write(b':ST'+command.encode()+b'#')  # command to start tracking
        response = self.ser.readline()
        packet = response.decode()
        if packet != '1':
            print('Error: Command rejected')
        return packet

    def calibrate(self):
        self.ser.write(b':CM#')  # command to calibrate
        response = self.ser.readline()
        packet = response.decode()
        if packet != '1':
            print('Error: we not calbrating today mf')
        return packet

    def slew_to_mech_zero(self):
        self.ser.write(b':MH#')  # slew to zero position
        response = self.ser.readline()
        packet = response.decode()
        if packet != '1':
            print('Error: we not going there home boi')
        return packet

    def stop_slew(self):
        self.ser.write(b':Q#')  # stop slewing
        response = self.ser.readline()
        packet = response.decode()
        if packet != '1':
            print('Error: we gon keep slewing')
        return packet

    def set_ra_dec(self, ra, dec):



        self.altaz = False

        ra = ra * (1000)  # this goes from s to ms
        ra = round(ra)
        self.ra = ra
        ra = str(ra)
        ra = ra.rjust(8, '0')

        dec = dec * 360000
        dec = round(dec)
        self.dec = dec
        if dec >= 0:
            signstr = '+'
        else:
            signstr = '-'
        dec = abs(dec)
        dec = str(dec)
        dec = dec.rjust(8, '0')

        self.ser.write(b':Sr' + ra.encode() + b'#')  # RA command
        response1 = self.ser.readline()
        packet1 = response1.decode()
        if packet1 != "1":
            print("Error: RA command denied")

        self.ser.write(b':Sd' + signstr.encode() + dec.encode() + b'#')  # dec command
        response2 = self.ser.readline()
        packet2 = response1.decode()
        if packet2 != "1":
            print("Error: dec command denied")

    def current_ra_dec(self):
        self.ser.write(b':GEC#')
        response = self.ser.readline()
        packet = response.decode()
        return packet

    def set_mech_zero(self):
        self.ser.write(b':SZP#')
        response = self.ser.readline()
        packet = response.decode()
        return packet
