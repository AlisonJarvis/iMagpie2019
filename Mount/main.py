import time
from Mount import Mount

mount = Mount("/dev/tty.usbserial-AQ00LYCP",9600, 5)

#mount.calibrate()
# mount.slew_to_mech_zero()
# time.sleep(15)
mount.set_alt_az(45, 45)
mount.slew_to_coordinates()
mount.set_alt_az(60, 60)
mount.slew_to_coordinates()
mount.set_alt_az(15, 15)
mount.slew_to_coordinates()
mount.set_alt_az(90, 120)
mount.slew_to_coordinates()
mount.set_alt_az(75, 100)
mount.slew_to_coordinates()
print(mount.current_alt_az())
mount.slew_to_mech_zero()




