
# Operation: get the camera to call me daddy

# These packages were used by Daddy Marple
import argparse
import os
import sys
import time
import zwoasi as asi

#These ones were used for Raspberry Pi GPIO (sudo apt-get install python-rpi.gpio python3-rpi.gpio)
import RPi.GPIO as GPIO

# Function to save control values to text file (bc Daddy Marple told me to)
def save_control_values(filename, settings):
    filename += '.txt'
    with open(filename, 'w') as f:
        for k in sorted(settings.keys()):
            f.write('%s: %s\n' % (k, str(settings[k])))
    print('Camera settings saved to %s' % filename)

# Set Raspberry pi GPIO pin stuff for Calibration mode
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set BCM 11 to be an input pin and set initial value to be pulled low (off)

# Get environment variable key (bc Daddy Marple told me to)
env_filename = os.getenv('ZWO_ASI_LIB')

# Process and Save Images from camera (bc Daddy Marple told me to)
parser = argparse.ArgumentParser(description='Process and save images from a camera')
parser.add_argument('filename',
                    nargs='?',
                    help='SDK library filename')
args = parser.parse_args()

# Initialize zwoasi w/ name of the SDK library (bc Daddy Marple told me to)
if args.filename:
    asi.init(args.filename)
elif env_filename:
    asi.init(env_filename)
else:
    print('The filename of the SDK library is required (or set ZWO_ASI_LIB environment variable with the filename)')
    sys.exit(1)

# Get the number of attached cameras (bc Daddy Marple told me to)
num_cameras = asi.get_num_cameras()
if num_cameras == 0:
    print('No cameras found')
    sys.exit(0)

# Get the list of model names for cameras connected (bc Daddy Marple told me to)
cameras_found = asi.list_cameras()

if num_cameras == 1:
    camera_id = 0
    print('Found one camera: %s' % cameras_found[0])
else:
    print('You got too many cameras homie')

camera = asi.Camera(camera_id)
camera_info = camera.get_camera_property()

# Get all of the camera controls (bc Daddy Marple told me to)
print('')
print('Camera controls:')
controls = camera.get_controls()
for cn in sorted(controls.keys()):
    print('    %s:' % cn)
    for k in sorted(controls[cn].keys()):
        print('        %s: %s' % (k, repr(controls[cn][k])))

# Use minimum USB bandwidth permitted (bc Daddy Marple told me to)
camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MinValue'])

# Set Defaults for camera (bc Daddy Marple told me to)
# **They will need adjusting depending upon the sensitivity, lens and lighting conditions used.**

camera.disable_dark_subtract()

camera.set_control_value(asi.ASI_GAIN, 150)
camera.set_control_value(asi.ASI_EXPOSURE, 30000)
camera.set_control_value(asi.ASI_WB_B, 99)
camera.set_control_value(asi.ASI_WB_R, 75)
camera.set_control_value(asi.ASI_GAMMA, 50)
camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
camera.set_control_value(asi.ASI_FLIP, 0)

# Force any single exposure to be halted
try:
    camera.stop_video_capture()
    camera.stop_exposure()
except (KeyboardInterrupt, SystemExit):
    raise
except:
    pass

#Open that shit (if applicable?)
camera._open_camera()

# We will need to receive commanded exposure time from the provided queue
start_exp_time = 1
stop_exp_time = 2

# Run a continuous loop that waits for camera commands
while True:

    time = 0 # Time variable will either require constant communication with the GSM (more accurate)
    # or constant incrementation of a variable with help from the raspberry pi internal clock (may not be as accurate)

    while GPIO.input(11) == GPIO.HIGH: #Run while calibration mode is enabled
        camera._start_video_capture() #Or continuously take photos? There are algorithms to display images to full screen

    if time == com_exp_time #Begin exposure if next time in queue is reached
        camera._start_exposure()
        while time != stop_exp_time
            #Need to constantly increment time value by methods outlined above

        camera._stop_exposure()

        #Find out how to save the images and send them to the image processing code


# Close that shit
camera._close_camera()
