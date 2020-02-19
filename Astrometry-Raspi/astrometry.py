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
output = proc.communicate()[0] #communicate with the opened process
output = output.split("\n") #parsing into each line
#output = output[0].split("\\") #dunno i was told this one
"""
for line in output: #parse line by line
    RA_Dec_index = output.find("Field center: (RA,Dec) =") #find when it solves to give field center
    Field_rotation_index = output.find("Field rotation angle:") #find when it solves to give rotation angle
print("RA and Dec index = " + str(RA_Dec_index)) #find index with meaningful data
print("Field Rotation angle index = " + str(Field_rotation_index)) #find index with meaningful data
#print("RA and Dec Value = " +str
"""""

for line in output:
    if line.find("Field center: (RA,Dec) ="):
        RA_Dec_Line = line
    if line.find("Field rotation angle:"):
        Rot_Angle_Line = line
        break

print(RA_Dec_Line)
print(Rot_Angle_Line)
