import time
from Mount import Mount

mount = Mount("/dev/ttyUSB0",9600, 5)

#mount.calibrate()
mount.slew_to_mech_zero()
time.sleep(15)
mount.set_alt_az(90, 45)
mount.slew_to_coordinates()
time.sleep(20)
mount.stop_slew()
print(mount.current_alt_az())



