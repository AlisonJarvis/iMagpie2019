from GSM import GSM
gsm = GSM("/dev/ttyUSB0",9600, 5)
set_mes = gsm.set_to_sms()
print(set_msg)
# print(gsm.read_msg(0,0))
num = "+172034662942"
msg = "Hello"
pack1, pack2 = gsm.send_sms(num, msg)
print(pack1)
print(pack2)