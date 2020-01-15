##################################################################
# iMagpie: Sensor Code
# Created: 12/22/2019
# Modified: 12/22/2019
# Purpose: Functions to read and record sensor data
##################################################################
import board
import busio
import adafruit_bme280

# create board i2c object
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# defines temp sensor device ids
device_file = ['/sys/bus/w1/devices/28-000009958138/w1_slave','/sys/bus/w1/devices/28-000009957683/w1_slave','/sys/bus/w1/devices/28-000009958549/w1_slave','/sys/bus/w1/devices/28-0000099577b3/w1_slave','/sys/bus/w1/devices/28-00000995861d/w1_slave','/sys/bus/w1/devices/28-0000099566dc/w1_slave','/sys/bus/w1/devices/28-000009957c5d/w1_slave','/sys/bus/w1/devices/28-00000995853b/w1_slave','/sys/bus/w1/devices/28-000009957f18/w1_slave']
num_temp = len(device_file)

# create adc object
adc = Adafruit_ADS1x15.ADS1015()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

# reads environmental sensors
def env_sensors():
	print("\nTemperature: %0.1f C" % bme280.temperature)
	print("Humidity: %0.1f %%" % bme280.humidity)
	print("Pressure: %0.1f kPa" % bme280.pressure/10)

# reads temp from each sensor
def read_temp():
	temp_c = ()
	for i in range(0,num_temp):
		f = open(device_file[i], 'r')
		lines = f.readlines()
		f.close()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = temp_c + (float(temp_string)/1000.0,)
	return temp_c

