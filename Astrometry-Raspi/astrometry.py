#!C:\iMagpie\venv\Scripts\python.exe
# #import os #for using terminal
import subprocess #for getting data out of terminal output

RA = 13.43306 #Right Ascension in degrees
DEC = -10.82389 #Declination in degrees
radius = 5 #radius in degrees of what to search around center RA and DEC
Low = 5 #lower bound of arc second per pixel of picture
Hi = 5.5 #Upper bound of arc second per pixel of picture
sample = 2 #downsample the picture by this factor first before solving


cmd = "./solve-field --ra %f --dec %f --radius %f -L %f -H %f -u arcsecperpix --downsample %d --no-plots -D ~/Desktop/_APP3220.solvage ~/Desktop/_APP3220.solvage/_APP3220.jpg" % (RA,DEC,radius,Low,Hi,sample,)
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) #saving terminal output to variables within python
# os.system("cmd") #execute astrometry terminal command
output = proc.communicate()[0]
output = output.split("\n")
output = output[0].split("\\")

for line in output:
    RA_Dec_index = output.find("Field center: (RA,Dec) =")
    Field_rotation_index = output.find("Field rotation angle:")
print("RA and Dec index = " + str(RA_Dec_index))
print("Field Rotation angle index = " + str(Field_rotation_index))
#print("RA and Dec Value = " +str