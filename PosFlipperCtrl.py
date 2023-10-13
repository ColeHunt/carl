"""
PosFlipperCtrl.py

Description: Control method for flipper control via position
Author: Dustin Fouts
Date: 9/27/23

"""

from SparkCANLib import SparkController

# CAN IDs for Flipper Controllers
FLF = 21
FRF = 22
RLF = 23
RRF = 24

# Factor to scale Rotate Position
FACTOR = 1

class Flipper:
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

    def setFlipperPosition(self, position):
        self.controller.position_output(position)

    def rotateFlipperPosition(self, control):
        desired_position = self.getPosition() + control * FACTOR
        self.setFlipperPosition(desired_position)

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

    def rotateSystemPosition(self, fl, fr, rl, rr, update):
        self.FLFlipper.rotateFlipperPosition(fl * update)
        self.FRFlipper.rotateFlipperPosition(fr * update)
        self.RLFlipper.rotateFlipperPosition(rl * update)
        self.RRFlipper.rotateFlipperPosition(rr * update)

    def setSystemPositions(self, fl, fr, rl, rr):
        self.FLFlipper.setFlipperPosition(fl)
        self.FRFlipper.setFlipperPosition(fr)
        self.RLFlipper.setFlipperPosition(rl)
        self.RRFlipper.setFlipperPosition(rr)

    def disable(self):
        self.FLFlipper.setFlipperPosition(0)
        self.FRFlipper.setFlipperPosition(0)
        self.RLFlipper.setFlipperPosition(0)
        self.RRFlipper.setFlipperPosition(0)

   # def hold(self, fl, fr, rl, rr): 
        self.FLFlipper.setFlipperPosition(fl.getPosition())
        self.FRFlipper.setFlipperPosition(fr)
        self.RLFlipper.setFlipperPosition(rl)
        self.RRFlipper.setFlipperPosition(rr)


    def getSystemPositions(self):
        print(f"FLF: {self.FLFlipper.getPosition()}, FRF: {self.FRFlipper.getPosition()}, RLR: {self.RLFlipper.getPosition()}, RRF: {self.RRFlipper.getPosition()}")
