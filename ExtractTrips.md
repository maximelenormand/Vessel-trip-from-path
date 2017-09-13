Extract trips from spatio-temporal vessels' paths
========================================================================

## Description

This script divides spatio-temporal vessels's paths (i.e. collection of spatio-temporal positions sorted by time) into trips based on the following definition:

"A trip is composed of at least three successive positions being farther than ***thd*** meters from the coast 
and separated by inverevent times lower than ***tht*** seconds."

## Input

The algorithm takes as input a 5 columns csv file with column names, **the value separator is a semicolon ";"**.
Each row of the file represents a spatio-temporal position of a vessel's path. 

It is important to note that the table must be **SORTED** by ID and by time.

1. **Vessel ID**
2. **Unix Time**
3. **X:** cartesian coordinate (in meters) 
4. **Y:** cartesian coordinate (in meters) 
5. **DistLand:** Distance from the nearest land (in meters) 

## Parameters
 
The algorithm has 5 parameters:

1. **wdinput:**  Path of the input file
2. **wdoutput:** Path of the output file
3. **thd:** Distance threshold (in meters)
4. **tht:** Time threshold (in seconds)
5. **epsilon:** maximum distance (in meters) between the simplified path and the original one (Ramer–Douglas–Peucker algorithm)

## Output

The algorithm returns a 10 columns csv file with column names, **the value separator is a semicolon ";"**. 

1. **ID of the vessel**
2. **ID of the trip**
3. **Unix Time**
4. **X:** cartesian coordinate (in meters) 
5. **Y:** cartesian coordinate (in meters) 
6. **DistLand:** Distance from the nearest land (in meters)  
7. **Delta_t:** Time ellapsed between the last and the current position (in seconds) 
8. **Delta_d:** Distance traveled between the last and the current position (in meters)
9. **Theta:**  Angle between the last, the current and the next position (in degree). Negative for left and positive for right.
10. **Simplified:** 1 if the position is on the simplified trajectory (Ramer–Douglas–Peucker algorithm), 0 otherwise
