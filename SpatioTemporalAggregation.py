# -*- coding: utf-8 -*-

"""
Spatio-temporal aggregation of vessels' trips

The aim of this script is to spatially aggregate a vessel trip over a spatial distribution of polygons according to a simplified 
trajectory. A trip is composed of exact spatio-temporal positions (T, X, Y) spatially included in a spatial polygon. A trip can also 
be simplified with a Ramer–Douglas–Peucker algorithm for example. In this case only polygons containing at least one position in the 
simplified trip will be considered.  
 
All the position successively located in the same polygon are aggregated into one single position (i.e. polygon). All the 
positions' attributes are averaged over the different positions. The time spent into the polygon is equal to the ellapsed between the 
arrival time and departure time from the polygon. The arrival time is approximated by the time between the first position in the polygon 
and the previous one.The departure time is approximated by the time between the last position in the polygon and the next one. 

The algorithm takes as input a 8 columns csv file with column names (the value separator is a semicolon ";"). Each row of the file 
represents a spatio-temporal position of a vessel's trajectory. 

It is important to note that the table must be SORTED by Trip ID and by time, and each trip should be composed of at least 3 positions. 
 
	1. Trip ID
	2. Unix Time
	3. X cartesian coordinate (in meters)
	4. Y cartesian coordinate (in meters)
	5. DistLand: Distance from the nearest land (in meters)
	6. Speed (in meter/second)
	7. Simplified: 1 if the position is on a simplified trip
                     0 otherwise
	8. ID polygon                    
 
The algorithm has 5 parameters:

	1. wdinput:  Path of the input file
	2. wdoutput: Path of the output file

The algorithm returns a 10 columns csv file with column names (the value separator is a semicolon ";"). Each row of the file represents 
a spatio-temporal aggregate position of a vessel's simplified trip. 


	1. Trip ID
	2. ID polygon  
	3. Unix Time
	4. X cartesian coordinate (in meters)
	5. Y cartesian coordinate (in meters)
	6. DistLand: Distance from the nearest land (in meters)
	7. Delta_t: Time ellapsed between the last and the current aggregate position (in seconds)
	8. Delta_d: Distance traveled between the last and the current aggregate position (in meters)
	9. Theta: Turning angle based on the change of direction between the last, the current and the next aggregate position (in degree). 
                Negative for left and positive for right.
	10. Time: Time spent in the polygon (in seconds)                

Copyright 2016 Maxime Lenormand. All rights reserved. Code under License GPLv3.
"""

# ****************************** IMPORTS **************************************************************************************************
# *****************************************************************************************************************************************

import sys
import math

# ****************************** PARAMETRES ***********************************************************************************************
# *****************************************************************************************************************************************

wdinput = sys.argv[1]
wdoutput = sys.argv[2]

print(" ") 
print("Parameters:" + " "+ wdinput + " " + wdoutput)
print(" ") 

# ********************************************* LOAD FUNCTIONS ***************************************************************************
# ****************************************************************************************************************************************

#Euclidean distance bebween (x0, y0) and (x1, y1)
def disteucl(x0, y0, x1, y1):
    return  math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

   
# ****************************** MAIN *****************************************************************************************************
# *****************************************************************************************************************************************

#Input file                                        
input_file = open(wdinput)                                 #Open file 
next(input_file)                                           #Skip column names

input_file2 = open(wdinput)                                #Open the file again to detect the next vessel ID
next(input_file2)                                          #Skip column names
next(input_file2)                                          #Skip first position

#Output file
output_file = open(wdoutput,'w')
output_file.write('Trip ID')
output_file.write(';')
output_file.write('ID polygon')
output_file.write(';')
output_file.write('Unix Time')
output_file.write(';')
output_file.write('X')
output_file.write(';')
output_file.write('Y')
output_file.write(';')
output_file.write('DistLand')
output_file.write(';')
output_file.write('Speed')
output_file.write(';')
output_file.write('Delta_t')
output_file.write(';')
output_file.write('Delta_d')
output_file.write(';')
output_file.write('Theta')
output_file.write(';')
output_file.write('Time')
output_file.write('\n')

#Firstline of the vessel trajectory 
firstline = True

#Looping through the file line by line
for line in input_file:
        
    #Trip's position attributes
    attr = line.rstrip('\n\r').split(';')                         #Split line
    ID = attr[0]                                                  #Trip ID
    time = int(attr[1])                                           #Unix Time
    x = float(attr[2].replace(',', '.'))                          #X cartesian coordinate
    y = float(attr[3].replace(',', '.'))                          #Y cartesian coordinatecoordinate
    land = float(attr[4].replace(',', '.'))                       #Distance to Land
    speed = float(attr[5].replace(',', '.'))                      #Speed
    simpl = int(attr[6].replace(',', '.'))                        #Simplified?    
    polID = attr[7]                                               #Polygon ID 
    
    #Next Trip ID
    try:
        attr = next(input_file2).rstrip('\n\r').split(';')
        ID_next = attr[0]                                         #Vessel ID                                   
    except(StopIteration):
        ID_next = ID + "last"                                     #Fake ID if last line
    
    #IF first vessel's position 
    #THEN initialize variables    
    if firstline:

        #Trip description
        muT = [time]                            #Sum time based on successive positions in the polygon
        minT = [time]                           #Arrival time to the polygon 
        maxT = [time]                           #Departure time from the polygon       
        muX = [x]                               #Sum X coordinate based on successive positions in the polygon
        muY = [y]                               #Sum Y coordinate based on successive positions in the polygon
        muL = [land]                            #Sum dist to land based on successive positions in the polygon
        muSp = [speed]                          #Sum speed in the polygon
        muSi = [simpl]                          #Number of positions in the simplified trip in the polygon 
        P = [polID]                             #Polygon ID
        count = [1]                             #Number of position in the polygon (to compute the averages)
        
        #Update firstline
        firstline = False
            
    else:

       #IF same polygon 
       #THEN update trip by aggregation        
       if polID == P[-1]:
           
           muT[-1] += time
           maxT[-1] = time
           muX[-1] += x
           muY[-1] += y
           muL[-1] += land
           muSp[-1] += speed
           muSi[-1] += simpl
           count[-1] +=1
       
       #ELSE add a position
       else:
           
           mint = maxT[-1]
           maxT[-1] = maxT[-1] + (time - maxT[-1]) / 2
           
           #Remove last position if not in the simplified trajectory
           if muSi[-1] == 0:
               muT = muT[:-1]
               minT = minT[:-1]
               maxT = maxT[:-1]
               muX = muX[:-1]
               muY = muY[:-1]
               muL = muL[:-1]
               muSp = muSp[:-1]
               muSi = muSi[:-1]
               P = P[:-1]
               count = count[:-1]

           muT = muT + [time]                            
           minT = minT + [mint + (time - mint) / 2]                           
           maxT = maxT + [time]                                   
           muX = muX + [x]                             
           muY = muY + [y]                             
           muL = muL + [land]                            
           muSp = muSp + [speed]                        
           muSi = muSi + [simpl]                        
           P = P + [polID]                          
           count = count + [1]                                  
       
       #IF last position
       #THEN write the output
       if ID != ID_next:
                      
           for i in range(0, len(P)):
               
               #Compute the average
               muT[i] = muT[i] / count[i]
               muX[i] = muX[i] / count[i]
               muY[i] = muY[i] / count[i]
               muL[i] = muL[i] / count[i]
               muSp[i] = muSp[i] / count[i]
               
               output_file.write(ID)                                   
               output_file.write(';')
               output_file.write(P[i])
               output_file.write(';')
               output_file.write(str(muT[i]))
               output_file.write(';')
               output_file.write(str(muX[i]))
               output_file.write(';')
               output_file.write(str(muY[i]))
               output_file.write(';')
               output_file.write(str(muL[i]))
               output_file.write(';')
               output_file.write(str(muSp[i]))
               output_file.write(';')
               
               if i==0:
                   output_file.write(str(0))     
                   output_file.write(';')
                   output_file.write(str(0))     
                   output_file.write(';')
                   output_file.write(str(0)) 
                   output_file.write(';')

               else:
                   #Compute interevent time and distance                                                                                       
                   output_file.write(str(muT[i] - muT[(i-1)]))
                   output_file.write(';')
                   output_file.write(str(disteucl(muX[i], muY[i], muX[(i-1)], muY[(i-1)])))
                   output_file.write(';')

                   if i == (len(P)-1):
                       output_file.write(str(0))
                       output_file.write(';')
                   #Compute angle    
                   else:
                       #Coordinate and norm vector a and b
                       Xa = muX[i]-muX[(i+1)]
                       Ya = muY[i]-muY[(i+1)]          
                       Xb = muX[i]-muX[(i-1)]
                       Yb = muY[i]-muY[(i-1)]
                       Na = math.sqrt(Xa**2+Ya**2);
                       Nb = math.sqrt(Xb**2+Yb**2);
                       
                       #If same position
                       if(Na==0 or Nb==0):
                           output_file.write(str(0))
                       else:    
                           cos = (Xa*Xb+Ya*Yb)/(Na*Nb)
                           if cos < -1:
                               cos = -1
                           if cos >1:
                               cos = 1
                               
                           sin = (Xa*Yb-Ya*Xb)
                           if sin < 0:
                               output_file.write(str(180-math.acos(cos)*(180./math.pi)))
                           else:
                               output_file.write(str(-180+math.acos(cos)*(180./math.pi)))
                       output_file.write(';')
               #Compute time spent in the polygon                                                      
               output_file.write(str(maxT[i] - minT[i])) 
               output_file.write('\n')   
                                 
           firstline = True
             
#Close files
input_file.close()
input_file2.close()
output_file.close()

#End
print("End of the process")  
