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
        return packet
