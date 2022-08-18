from abc import ABCMeta, ABC, abstractmethod

class Component(metaclass = ABCMeta):
    @abstractmethod
    def move(self):
        pass

class Arm(Component):
    def __init__(self):
        pass
arm = Arm()
class Gripper:
    def __init__(self):
        pass
class LocationTracker():
    def __init__(self):
        pass

class Base:
    def __init__(self):
        pass