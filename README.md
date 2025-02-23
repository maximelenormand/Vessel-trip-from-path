# Extract and aggregate trips from spatio-temporal vessel paths

## Description

This repository provides two scripts, ***ExtractTrips.py*** and 
***SpatialAggregation.py***, to extract and aggregate trips from spatiotemporal 
vessel paths.

***ExtractTrips.py*** divides spatio-temporal vessels's paths (i.e. collection 
of spatio-temporal positions sorted by time) into trips. A trip is composed of 
at least three successive positions being farther than ***thd*** meters from 
the coast and separated by inverevent times lower than ***tht*** seconds.

***SpatialAggregation.py*** spatially aggregate a vessel trip over a spatial 
distribution of polygons according to a simplified trip. A trip is composed 
of exact spatio-temporal positions (T, X, Y) spatially included in a spatial 
polygon. A trip can also be simplified with a Ramer–Douglas–Peucker algorithm 
for example. In this case only polygons containing at least one position in 
the simplified trip will be considered. All the positions successively located 
in the same polygon are aggregated in order to obtain an aggregate position
characterized by time, geographical coordinates and speed averaged over the 
successive records. The time spent into the polygon is equal to the time 
elapsed between the arrival time and departure time from the polygon. 
The arrival time is approximated by the time between the first position in 
the polygon and the previous one. The departure time is approximated by 
the time between the last position in the polygon and the next one.

## Extract trips from spatio-temporal vessel paths

### Inputs

The algorithm takes as input a 5 columns csv file with column names, 
**the value separator is a semicolon ";"**.
Each row of the file represents a spatio-temporal position of a vessel's path. 

It is important to note that the table must be **SORTED** by ID and by time.

1. **Vessel ID**
2. **Unix Time**
3. **X:** cartesian coordinate (in meters) 
4. **Y:** cartesian coordinate (in meters) 
5. **DistLand:** Distance from the nearest land (in meters) 

### Parameters
 
The algorithm has 5 parameters:

1. **wdinput:**  Path of the input file
2. **wdoutput:** Path of the output file
3. **thd:** Distance threshold (in meters)
4. **tht:** Time threshold (in seconds)
5. **epsilon:** maximum distance (in meters) between the simplified path and the original one (Ramer–Douglas–Peucker algorithm)

### Output

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

## Spatial aggregation of vessel trips

### Inputs

The algorithm takes as input a 8 columns csv file with column names 
(the value separator is a semicolon ";"). Each row of the file represents a 
spatio-temporal position of a vessel's trip. 

It is important to note that the table must be SORTED by Trip ID and by time, 
each trip should be composed of at least 3 positions.

1. **Trip ID**
2. **Unix Time**
3. **X:** cartesian coordinate (in meters)
4. **Y:** cartesian coordinate (in meters)
5. **DistLand:** Distance from the nearest land (in meters) 
6. **Speed** 
7. **Simplified:** 1 if the position is on a simplified trip, 0 otherwise
8. **Polygon ID**

### Parameters
 
The algorithm has 2 parameters:

1. **wdinput:**  Path of the input file
2. **wdoutput:** Path of the output file

### Output

The algorithm returns a 10 columns csv file with column names, 
**the value separator is a semicolon ";"**. Each row of the file represents a 
spatio-temporal aggregate position of a vessel's simplified trip. 

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


## Execution

You can run the scripts using the command:

**python ExtractTrips.py input.csv output.csv 4000 36000 300**

and

**python SpatialAggregation.py input.csv output.csv**

If you need help, find a bug, want to give me advice or feedback, please contact me!

## Repository mirrors

This repository is mirrored on both GitLab and GitHub. You can access it via the following links:

- **GitLab**: [https://gitlab.com/maximelenormand/Vessel-trip-from-path](https://gitlab.com/maximelenormand/Vessel-trip-from-path)  
- **GitHub**: [https://github.com/maximelenormand/Vessel-trip-from-path](https://github.com/maximelenormand/Vessel-trip-from-path)  

The repository is archived in Software Heritage:

[![SWH](https://archive.softwareheritage.org/badge/origin/https://github.com/maximelenormand/Vessel-trip-from-path/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/maximelenormand/Vessel-trip-from-path)

