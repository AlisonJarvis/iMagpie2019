import time
from Mount import Mount
from GSM import GSM

mount = Mount("/dev/tty.usbserial-AQ00LYCP",9600, 5)
gsm = GSM("/dev/tty.usbserial-AQ00LYCP",9600, 5)

