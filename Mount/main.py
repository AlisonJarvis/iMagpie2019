import time
from Mount import Mount

mount = Mount("/dev/tty.usbserial-AQ00LYCP",9600, 5)

#mount.calibrate()
mount.slew_to_mech_zero()
time.sleep(15)
mount.set_alt_limit('-89')
print(mount.current_alt_limit())
mount.set_alt_az(45, 45)
mount.calibrate()
mount.slew_to_coordinates()
#altaz = mount.current_alt_az
#while altaz != "['+45.0', '45.0']":
#    mount.stop_slew()
#    break
time.sleep(20)
mount.stop_slew()
print(mount.current_alt_az())



