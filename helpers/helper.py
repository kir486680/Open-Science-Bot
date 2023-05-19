import numpy as np



#gear diameter is 4.2
def rotationsToDistance(rotations, diameter):
    return np.pi*diameter
def degreesToDistance(degrees, diameter):
    distancePerDegree = np.pi * diameter / 360
    return distancePerDegree * degrees
def dist2deg(desiredDistance, diameter):
    distancePerDegree = (np.pi * diameter) / 360
    return desiredDistance/distancePerDegree
