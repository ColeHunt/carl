#!/usr/bin/python3

"""
teleop.py

Desc: Main control loop for carl operation
Author: Cole Hunt
Date: 4/14/23

"""

from driveTrain import DriveTrain
from SparkCANLib import SparkCAN
from flipperControl import FlipperControl
from operatorInterface import OI
import time

ENABLED = True

def main():

    # Create Operatior Interface object
    oi = OI()

    #Instantiate SparkBus object
    bus = SparkCAN.SparkBus(channel="can0", bustype='socketcan', bitrate=1000000)

    driveTrainObj = DriveTrain(bus)
    flipperControlObj = FlipperControl(bus)
    flipperControlObj.setSystemHome()

    while(ENABLED):
        time.sleep(0.05)
        driveTrainObj.arcadeDrive(oi.getLeftJoystickXAxis(), oi.getLeftJoystickYAxis())
        flipperControlObj.rotateSystemPercentOutput(oi.getLeftBumperPressed(), oi.getRightBumperPressed(), oi.getLeftTriggerAxis(), oi.getRightTriggerAxis(), oi.getRightJoystickYAxis())
        if(oi.getStartButtonPressed()):
            flipperControlObj.returnSystemToHome()

if __name__ == "__main__":
    main()
