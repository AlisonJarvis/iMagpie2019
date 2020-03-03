from GSM import GSM
gsm = GSM("/dev/tty.usbserial-AQ00LYCP",9600, 5)
gsm.set_to_sms()
print(gsm.read_msg())
