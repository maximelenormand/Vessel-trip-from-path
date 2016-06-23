Spatial aggregation of vessels' trips
========================================================================

 Copyright 2016 Maxime Lenormand. All rights reserved. Code under License GPLv3.
______________________________________________________________________________________

## Description

The aim of this script is to spatially aggregate a vessel trip over a spatial distribution of polygons according to a simplified trip. A trip is composed of exact spatio-temporal positions (T, X, Y) spatially included in a spatial polygon. A trip can also be simplified with a Ramer–Douglas–Peucker algorithm for example. In this case only polygons containing at least one position in the simplified trip will be considered.  

All the positions successively located in the same polygon are aggregated in order to obtain an aggregate position characterized by time, geographical coordinates and speed averaged over the successive records. The time spent into the polygon is equal to the time elapsed between the arrival time and departure time from the polygon. The arrival time is approximated by the time between the first position in the polygon and the previous one. The departure time is approximated by the time between the last position in the polygon and the next one. 

## Input

The algorithm takes as input a 8 columns csv file with column names (the value separator is a semicolon ";"). Each row of the file represents a spatio-temporal position of a vessel's trip. 

It is important to note that the table must be SORTED by Trip ID and by time, each trip should be composed of at least 3 positions.

1. **Trip ID**
2. **Unix Time**
3. **X:** cartesian coordinate (in meters)
4. **Y:** cartesian coordinate (in meters)
5. **DistLand:** Distance from the nearest land (in meters) 
6. **Speed** 
7. **Simplified:** 1 if the position is on a simplified trip, 0 otherwise
8. **Polygon ID**

## Parameters
 
The algorithm has 2 parameters:

1. **wdinput:**  Path of the input file
2. **wdoutput:** Path of the output file

## Output

The algorithm returns a 10 columns csv file with column names, **the value separator is a semicolon ";"**. Each row of the file represents a spatio-temporal aggregate position of a vessel's simplified trip. 

1. **Trip ID**
2. **Polygon ID**
3. **Unix Time**
4. **X:** cartesian coordinate (in meters)
5. **Y:** cartesian coordinate (in meters)
6. **DistLand:** Distance from the nearest land (in meters)  
7. **Delta_t:** Time ellapsed between the last and the current aggregate position (in seconds)
8. **Delta_d:** Distance traveled between the last and the current aggregate position (in meters)
9. **Theta:**  Turning angle based on the change of direction between the last, the current and the aggregate position (in degree). Negative for left and positive for right.
10. **Time:** Time spent in the polygon (in seconds) 
