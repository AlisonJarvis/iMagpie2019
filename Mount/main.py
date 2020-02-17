from Mount import ASCOMDriver as ASCOM

print("starting calibration...")
ASCOM.calibrate()
print("calibration done")

print("starting actuation...")
ASCOM.driver(45.0, 180.0)
print("actuation complete")

