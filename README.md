Extract fishing trips from spatio-temporal vessels' trajectories
========================================================================

 Copyright 2015 Maxime Lenormand. All rights reserved. Code under License GPLv3.
______________________________________________________________________________________

This script divides the spatio-temporal trajectory of a vessel into trips based on the following definition:

"A trip is composed of at least three successive positions being farther than *thd* meters from the coast 
and separated by inverevent times lower than *tht* seconds."

## Input

The algorithm takes as input a 5 columns csv file with column names, **the value separator is a semicolon ";"**.
Each row of the file represents a spatio-temporal position of a vessel's trajectory. 

It is important to note that the table must be **SORTED** by ID and by time.

1. **ID of the vessel**
2. **Unix Time**
3. **X cartesian coordinate**
4. **Y cartesian coordinate**
5. **DistLand:** Distance from the nearest land (in meters) 

## Parameters
 
The algorithm has 4 parameters:

1. **wdinput:**  Path of the input file (ex: "input.csv")
2. **wdoutput:** Path of the output file (ex: "outputoftheawsomemaximelenormandsalgorithm.csv")
3. **thd:** Distance threshold (in meters)
4. **tht:** Time threshold (in seconds)

## Output

The algorithm returns a 9 columns csv file with column names, **the value separator is a semicolon ";"**. 

1. **ID of the vessel**
2. **ID of the trip**
3. **Unix Time**
4. **X cartesian coordinate**
5. **Y cartesian coordinate**
6. **DistLand:** Distance from the nearest land (in meters)  
7. **Delta_t:** Time ellapsed between the last and the current location (in seconds) 
8. **Delta_d:** Distance traveled between the last and the current location (in meters)
9. **Theta:**  Angle between the last, the current and the next location (in degrees) 

## Execution

You can run the code using the command:

*python vesselTrajectories.py 'input.csv' 'output.csv' 4000 36000* 

## Citation

If you use this code, please cite:



If you need help, find a bug, want to give me advice or feedback, please contact me!
You can reach me at maxime.lenormand[at]irstea.fr

## References

