import serial
import time


class GSM:

    def __init__(self, port, baud, time_out):
        self.ser = serial.Serial(port, baud, timeout=time_out)

    def set_to_sms(self):
        self.ser.write(b"AT+CMGF=1")  # set to text mode
        response = self.ser.readline()
        packet = response.decode()
        return packet

    def del_sms(self, index, delflag):
        # index: integer, value in range of location numbers supported by associated memory
        self.ser.write(b'AT+CMGD=' + index.encode() + b'[,' + delflag.encode() + b']')  # delete SMS
        # delflag: 0: del msg specified by index
        #          1: Delete all read messages from preferred message storage,
        #             leaving unread messages and stored mobile originated
        #             messages (whether sent or not) untouched
        #          2: Delete all read messages from preferred message storage
        #             and sent mobile originated messages, leaving unread
        #             messages and unsent mobile originated messages
        #             untouched
        #          3: Delete all read messages from preferred message storage,
        #             sent and unsent mobile originated messages leaving
        #             unread messages untouched
        #          4: Delete all messages from preferred message storage
        #             including unread messages
        response = self.ser.readline()
        packet = response.decode()
        return packet

    def get_msg_from_store(self, stat, mode):
        # <stat> "REC UNREAD" Received unread messages
        #        "REC READ" Received read messages
        #        "STO UNSENT" Stored unsent messages
        #        "STO SENT" Stored sent messages
        #        "ALL" All messages
        self.ser.write(b'AT+CMGL=' + stat.encode() + b'[,' + mode.encode() + b']')
        # <mode> 0 Normal
        #        1 Not change status of the specified SMS record
        response = self.ser.readline()
        packet = response.decode()
        return packet

    def read_msg(self, index, mode):
        # <index> Integer type; value in the range of location numbers supported
        #         by the associated memory
        self.ser.write(b'AT+CMGR=' + index.encode() + b'[,' + mode.encode() + b']')
        # <mode> 0 Normal
        #        1 Not change status of the specified SMS record
        response = self.ser.readline()
        packet = response.decode()

        if packet == "GSMStatus":
            number = 'sdfd'
            self.check_status(1, number)
        return packet

    def send_sms(self, number, msg):
        str(number)
        self.ser.write(b'AT+CMGS=' + number.encode())  # send msg to number
        response = self.ser.readline()
        packet1 = response.decode()

        str(msg)
        self.ser.write(msg.encode())
        response = self.ser.readline()
        packet2 = response.decode()

        return packet1, packet2

    def check_status(self, mode, number):
        # mode is 1 for location, date/time
        #         2 for just date/time
        mode = str(mode)
        self.ser.write(b"AT+CIPGSMLOC=" + mode.encode())
        response = self.ser.readline()
        packet = response.decode()

        #sort packet for parameters
        if mode == '1':
            locationcode = packet[0:packet.find("[")]
            packet = packet[packet.find(',') + 1:-1] + ']'
            gsm_long = packet[0:packet.find(',')]
            packet = packet[packet.find(',') + 1:-1] + ']'
            gsm_lat = packet[0:packet.find(',')]
            packet = packet[packet.find(',') + 1:-1] + ']'
            gsm_date = packet[0:packet.find(',')]
            packet = packet[packet.find(',') + 1:-1] + ']'
            gsm_time = packet[0:-1]

            # error handling
            if locationcode == 0:
                msg = "GPS date and time: " + gsm_date + gsm_time + "GPS Location: " + "Longitude: " + gsm_long + "Latitude: " + gsm_lat
                # send message
                self.send_sms(number, msg)
            if locationcode == 404:
                msg = "Not Found"
                # send message
                self.send_sms(number, msg)
            if locationcode == 408:
                msg = "Request Timed Out"
                # send message
                self.send_sms(number, msg)
            if locationcode == 601:
                msg = "Network Error"
                # send message
                self.send_sms(number, msg)
            if locationcode == 602:
                msg = "No Memory"
                # send message
                self.send_sms(number, msg)
            if locationcode == 603:
                msg = "DNS Error"
                # send message
                self.send_sms(number, msg)
            if locationcode == 604:
                msg = "Stack Busy"
                # send message
                self.send_sms(number, msg)
            if locationcode == 65535:
                msg = "Other Error"
                # send message
                self.send_sms(number, msg)
            else:
                msg = "Error: no Location Code"
                # send message
                self.send_sms(number, msg)

            return locationcode, gsm_date, gsm_time, gsm_lat, gsm_long

        if mode == '2':
            locationcode = packet[0:packet.find("[")]
            packet = packet[packet.find(',') + 1:-1] + ']'
            gsm_date = packet[0:packet.find(',')]
            packet = packet[packet.find(',') + 1:-1] + ']'
            gsm_time = packet[0:-1]
            # error handling
            if locationcode == 0:
                msg = "GPS date and time: " + gsm_date + gsm_time
                # send message
                self.send_sms(number, msg)
            if locationcode == 404:
                msg = "Not Found"
                # send message
                self.send_sms(number, msg)
            if locationcode == 408:
                msg = "Request Timed Out"
                # send message
                self.send_sms(number, msg)
            if locationcode == 601:
                msg = "Network Error"
                # send message
                self.send_sms(number, msg)
            if locationcode == 602:
                msg = "No Memory"
                # send message
                self.send_sms(number, msg)
            if locationcode == 603:
                msg = "DNS Error"
                # send message
                self.send_sms(number, msg)
            if locationcode == 604:
                msg = "Stack Busy"
                # send message
                self.send_sms(number, msg)
            if locationcode == 65535:
                msg = "Other Error"
                # send message
                self.send_sms(number, msg)
            else:
                msg = "Error: no Location Code"
                # send message
                self.send_sms(number, msg)

            return locationcode, gsm_date, gsm_time

    def write_to_storage(self, number, msg):
        self.ser.write(b'AT+CMGW=' + number.encode())
        response = self.ser.readline()
        packet1 = response.decode()

        str(msg)
        self.ser.write(msg.encode())
        response = self.ser.readline()
        packet2 = response.decode()

        return packet1, packet2
