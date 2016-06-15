# -*- coding: utf-8 -*-

"""
Extract trips from spatio-temporal vessels' trajectories

This script divides spatio-temporal vessels's trajectories into trips based on the following definition:

"A trip is composed of at least three successive positions being farther than thd meters from the coast 
and separated by inverevent times lower than tht seconds."

The algorithm takes as input a 5 columns csv file with column names (the value separator is a semicolon ";").
Each row of the file represents a spatio-temporal position of a vessel's trajectory. 

It is important to note that the table must be SORTED by ID and by time.
 
	1. Vessel ID
	2. Unix Time
	3. X cartesian coordinate (in meters)
	4. Y cartesian coordinate (in meters)
	5. DistLand: Distance from the nearest land (in meters)
 
The algorithm has 5 parameters:

	1. wdinput:  Path of the input file
	2. wdoutput: Path of the output file
	3. thd: Distance threshold (in meters)
	4. tht: Time threshold (in seconds)
	5. epsilon: maximum distance (in meters) between the simplified trajectory and the original one (Ramer–Douglas–Peucker algorithm)

The algorithm returns a 10 columns csv file with column names (the value separator is a semicolon ";"). 

	1. Vessel ID
	2. Trip ID
	3. Unix Time
	4. X cartesian coordinate (in meters)
	5. Y cartesian coordinate (in meters)
	6. DistLand: Distance from the nearest land (in meters)
	7. Delta_t: Time ellapsed between the last and the current position (in seconds)
	8. Delta_d: Distance traveled between the last and the current position (in meters)
	9. Theta: Turning angle based on the change of direction between the last, the current and the next position (in degree). 
                Negative for left and positive for right.
	10. Simplified: 1 if the position is on the simplified trajectory (Ramer–Douglas–Peucker algorithm)
                      0 otherwise                

Copyright 2016 Maxime Lenormand. All rights reserved. Code under License GPLv3.
"""

# ****************************** IMPORTS **********************************************************************************************
# *************************************************************************************************************************************

import sys
import math

# ****************************** PARAMETRES *******************************************************************************************
# *************************************************************************************************************************************

wdinput = sys.argv[1]
wdoutput = sys.argv[2]
thd = float(sys.argv[3])
tht = float(sys.argv[4]) 
epsilon = float(sys.argv[5])

print(" ") 
print("Parameters:" + " "+ wdinput + " " + wdoutput + " " + str(thd) + " " + str(tht) + " " + str(epsilon))
print(" ") 

# ********************************************* LOAD FUNCTIONS ***********************************************************************
# ************************************************************************************************************************************

#Euclidean distance bebween (x0, y0) and (x1, y1)
def disteucl(x0, y0, x1, y1):
    return  math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

#Euclidean distance bebween (x0, y0) and the segment [(x1, y1), (x2,y2)]
def distpointline(x0, y0, x1, y1, x2, y2):
    if (x1 == x2 and y1==y2):
        return disteucl(x1, y1, x2, y2)
    else:
        return abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / disteucl(x1, y1, x2, y2)

#Ramer–Douglas–Peucker algorithm 
#Input: X, Y (two lists of cartesian coordinates in meters) and 
#       epsilon (maximum distance (in meters) between the simplified trajectory and the original one)
#Ouptu: S a list of length X giving for each position 1 if it is in the simplified trajectory and 0 otherwise    
def RDP(X, Y, epsilon):
    
    n = len(X)
    
    if epsilon > 0:
    
        dmax = 0.0
        index = 0
        
        for i in range(1, (n - 1)):
            d = distpointline(X[i], Y[i], X[0], Y[0], X[-1], Y[-1])
            if d > dmax:
                index = i
                dmax = d     
        if dmax >= epsilon:
            results = RDP(X[:index+1], Y[:index+1], epsilon)[:-1] + RDP(X[index:], Y[index:], epsilon)
        else:
            results = [0] * n
            results[0] = 1
            results[-1] = 1
    
    else:
        results = [1] * n        
        
    return results


   
# ****************************** MAIN *************************************************************************************************
# *************************************************************************************************************************************

#Input file                                        
input_file = open(wdinput)                                 #Open file 
next(input_file)                                           #Skip column names

input_file2 = open(wdinput)                                #Open the file again to detect the next vessel ID
next(input_file2)                                          #Skip column names
next(input_file2)                                          #Skip first position

#Output file
output_file = open(wdoutput,'w')
output_file.write('Vessel ID')                                   
output_file.write(';')
output_file.write('Trip ID')
output_file.write(';')
output_file.write('Unix Time')
output_file.write(';')
output_file.write('X')
output_file.write(';')
output_file.write('Y')
output_file.write(';')
output_file.write('DistLand')
output_file.write(';')
output_file.write('Delta_t')
output_file.write(';')
output_file.write('Delta_d')
output_file.write(';')
output_file.write('Theta')
output_file.write(';')
output_file.write('Simplified')
output_file.write('\n')

#Firstline of the vessel trajectory 
firstline = True

#Looping through the file line by line
for line in input_file:
    
    #Vessel's position attributes
    attr = line.rstrip('\n\r').split(';')                         #Split line
    ID = attr[0]                                                  #Vessel ID
    time = int(attr[1])                                           #Unix Time
    x = float(attr[2].replace(',', '.'))                          #X cartesian coordinate
    y = float(attr[3].replace(',', '.'))                          #Y cartesian coordinatecoordinate
    land = float(attr[4].replace(',', '.'))                       #Distance to Land
    
    test_t = True
    test_d = True
    
    #Next Vessel ID
    try:
        attr = next(input_file2).rstrip('\n\r').split(';')
        ID_next = attr[0]                                         #Vessel ID                                   
    except(StopIteration):
        ID_next = ID + "last"                                #Fake ID if last line
    
    #IF first vessel's position 
    #THEN initialize variables    
    if firstline:
        
        IDtrip = 0                       #ID trip        
        time_old = 0                     #Unix Time previous location 
        x_old = 0.0                      #X cartesian coordinate previous location 
        y_old = 0.0                      #Y cartesian coordinate previous location
        land_old = 0.0                   #Distance to land previous location 
        
        test_t = True                    #Test interevent time between current and last location lower than tht
        test_d = True                    #Test distance to land lower than thd
        test_t_old = False               #Test interevent time between last and last last location lower than tht
        test_d_old = (land > thd)        #Test distance to land previous location lower than thd

        #Trip
        T = []                           #Trip successive time
        X = []                           #Trip successive X coordinate 
        Y = []                           #Trip successive Y coordinate
        L = []                           #Trip successive distance to land
        
        firstline = False
        
    else:
       
       #Current time and distance tests        
       test_t = ((time-time_old) < tht)
       test_d = (land > thd)
       
       #IF the current position pass the tests AND the last one do not pass the tests AND not last position 
       #THEN start a new trip with the current position                  
       if ((test_t and test_d) and (not(test_t_old and test_d_old)) and (ID_next == ID)):
           #IF the previous position pass the distance test
           #THEN add the last position
           if (test_d_old):                              
               T = [time_old, time]        
               X = [x_old, x]         
               Y = [y_old, y]
               L = [land_old, land]
           else:
               T = [time]        
               X = [x]         
               Y = [y]
               L = [land]               
       #IF current and last positions pass the tests AND not last position 
       #THEN add current position        
       elif ((test_t and test_d) and (test_t_old and test_d_old) and (ID_next == ID)):
           T = T + [time]        
           X = X + [x]         
           Y = Y + [y]
           L = L + [land]
                                  
       #IF last position pass the tests AND current position not 
       #OR IF both last and current position pass the test AND last vessel position
       #THEN end the trip and write the results in the output file                           
       elif (((test_t_old and test_d_old) and (not(test_t and test_d))) or ((test_t_old and test_d_old) and (test_t and test_d) and (ID_next != ID))):
          
           #IF second condition
           #THEN add current position
           if ((test_t_old and test_d_old) and (test_t and test_d) and (ID_next != ID)):
               T = T + [time]        
               X = X + [x]         
               Y = Y + [y]
               L = L + [land]
               
           #IF more than three positions (to compute the angle)
           if (len(T) > 2):
               
               #Simplified trajectory with Ramer–Douglas–Peucker algorithm
               S = RDP(X, Y, epsilon) 
               
               #ID trip
               IDtrip += 1
               
               for i in range(0, len(T)):
                   
                   output_file.write(ID)                                   
                   output_file.write(';')
                   output_file.write(str(IDtrip))
                   output_file.write(';')
                   output_file.write(str(T[i]))
                   output_file.write(';')
                   output_file.write(str(X[i]))
                   output_file.write(';')
                   output_file.write(str(Y[i]))
                   output_file.write(';')
                   output_file.write(str(L[i]))
                   output_file.write(';')
                   
                   if i==0:
                       output_file.write(str(0))     
                       output_file.write(';')
                       output_file.write(str(0))     
                       output_file.write(';')
                       output_file.write(str(0)) 
                       output_file.write(';')
                       output_file.write(str(S[i]))                        
                       output_file.write('\n')
                   else:
                       #Compute interevent time and distance                                                                                       
                       output_file.write(str(T[i] - T[(i-1)]))
                       output_file.write(';')
                       output_file.write(str(disteucl(X[i], Y[i], X[(i-1)], Y[(i-1)])))
                       output_file.write(';')
    
                       if i==(len(T)-1):
                           output_file.write(str(0))
                           output_file.write(';')
                           output_file.write(str(S[i])) 
                           output_file.write('\n')
                       #Compute angle    
                       else:
                           #Coordinate and norm vector a and b
                           Xa = X[i]-X[(i+1)]
                           Ya = Y[i]-Y[(i+1)]          
                           Xb = X[i]-X[(i-1)]
                           Yb = Y[i]-Y[(i-1)]
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
                           output_file.write(str(S[i])) 
                           output_file.write('\n')   
       
       #Update test value
       test_t_old = test_t
       test_d_old = test_d
    
    #IF lastline 
    #THEN update firstline
    if ID_next != ID:
        firstline = True
    
    #Update position attribute                                                   
    time_old = time 
    x_old = x
    y_old = y
    land_old = land


#Close files
input_file.close()
input_file2.close()
output_file.close()

#End
print("End of the process")  
