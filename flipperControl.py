"""
flipperControl.py

Desc: Control Methods for flipper control
Author: Cole Hunt
Date: 4/14/23

"""

from SparkCANLib import SparkController

# CAN IDs for Flipper Controllers
FLF = 21
FRF = 22
RLF = 23
RRF = 24

# Factor to scale Rotate Speed
SCALE = 0.25

INVERTED = -1

# Factor to scale Rotate Position
FACTOR = 1

class Flipper:
    # Create a new controller for Flipper Motor Controller
    def __init__(self, bus, id):
        self.controller = bus.init_controller(id)
        self.setHome()

    def setHome(self):
        self.home = self.controller.position

    def goHome(self):
        self.controller.position_output(self.home)

    def setThresholds(self, upper, lower):
        self.upper = upper
        self.lower = lower

    def getPosition(self):
        return self.controller.position

    def inThreshold(self, update):
        if(((self.getPosition() + update * FACTOR) > self.upper)
           or ((self.getPosition() + update * FACTOR) < self.lower)):
            return False
        else:
            return True

    def rotateFlipperPosition(self, control):
        if(self.inThreshold(control)):
            self.controller.position_output(self.controller.postion + control * FACTOR)

    # Will be deprecated once position control is implemented
    def rotateFlipperPercentOutput(self, control):
        if(control != 0):
            self.controller.percent_output(control * SCALE)
        else:
            self.hold()

    # Will be deprecated once position control is implemented
    def hold(self):
        self.controller.velocity_output(0)


class FlipperControl:

    def __init__(self, bus):
        self.bus = bus
        # Front Left Drive Flipper
        self.FLFlipper = Flipper(bus, FLF)
        # Front Right Drive Flipper
        self.FRFlipper = Flipper(bus, FRF)
        # Rear Left Drive Flipper
        self.RLFlipper = Flipper(bus, RLF)
        # Rear Right Drive Flipper
        self.RRFlipper = Flipper(bus, RRF)

    def returnSystemToHome(self):
        self.FLFlipper.goHome()
        self.FRFlipper.goHome()
        self.RLFlipper.goHome()
        self.RRFlipper.goHome()

    def setSystemHome(self):
        self.FLFlipper.setHome()
        self.FRFlipper.setHome()
        self.RLFlipper.setHome()
        self.RRFlipper.setHome()

    def roateSystemPosition(self, fl, fr, rl, rr, update):
        self.FLFlipper.rotateFlipperPosition(fl * update)
        self.FRFlipper.rotateFlipperPosition(fr * update)
        self.RLFlipper.rotateFlipperPosition(rl * update)
        self.RRFlipper.rotateFlipperPosition(rr * update)

    # Will be deprecated once position control is implemented
    def rotateSystemPercentOutput(self, fl, fr, rl, rr, power):
        self.FLFlipper.rotateFlipperPercentOutput(fl * power * INVERTED)
        self.FRFlipper.rotateFlipperPercentOutput(fr * power)
        self.RLFlipper.rotateFlipperPercentOutput(rl * power)
        self.RRFlipper.rotateFlipperPercentOutput(rr * power * INVERTED)

    # Will be deprecated once position control is implemented
    def holdSystem(self):
        self.FLFlipper.hold()
        self.FRFlipper.hold()
        self.RLFlipper.hold()
        self.RRFlipper.hold()

    def disable(self):
        self.FLFlipper.rotateFlipperPercentOutput(0)
        self.FRFlipper.rotateFlipperPercentOutput(0)
        self.RLFlipper.rotateFlipperPercentOutput(0)
        self.RRFlipper.rotateFlipperPercentOutput(0)

    def getSystemPositions(self):
        print(f"FLF: {self.FLFlipper.getPosition()}, FRF: {self.FRFlipper.getPosition()}, RLR: {self.RLFlipper.getPosition()}, RRF: {self.RRFlipper.getPosition()}")



