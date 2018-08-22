'''
	Created on 2/3/2017.
	Objective: calculate Distance between Coordinates
	Created by : reh
'''
import math
def distanceFormula(p0,p1):
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
