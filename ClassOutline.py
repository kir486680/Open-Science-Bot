from abc import ABCMeta, ABC, abstractmethod
import numpy as np


class Component(metaclass = ABCMeta):
    @abstractmethod
    def move(self):
        pass
    def dist2deg(self, desiredDistance, diameter):
        distancePerDegree = np.pi * diameter / 360
        return desiredDistance/distancePerDegree


arm = Arm()

class Gripper(Component):
    
    def __init__(self, gripper):
        self.gripper = gripper
        self.pos = 0
    def grip(self):
        if self.pos == 0:
            self.gripper.run_for_degrees(-40,-30) #release
        else:
            self.gripper.run_for_degrees(40,30)
    def dist2deg(self, desiredDistance):
        return desiredDistance/0.02666667

class LocationTracker(Component):
    def move():
        pass
    def __init__(self):
        pass

class Base(Component):
    def __init__(self, base, gearDiam = 1.3):
        self.base = base
        self.gearDiam = gearDiam
        self.position = 0
    def move(self,distance):
        super().dist2deg(distance, self.gearDiam)