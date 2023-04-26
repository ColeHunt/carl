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

def main():

    # Create Operatior Interface object
    oiObj = OI()

    #Instantiate SparkBus object
    bus = SparkCAN.SparkBus(channel="can0", bustype='socketcan', bitrate=1000000)

    driveTrainObj = DriveTrain(bus)
    #flipperControlObj = FlipperControl(bus)

    while True:
        if(oiObj.isEnabled):
            controlLoop(driveTrainObj, oiObj)

def controlLoop(oiObj, driveTrainObj):
    driveTrainObj.arcadeDrive(oiObj.getLeftJoystickXAxis(), oiObj.getLeftJoystickYAxis())

if __name__ == "__main__":
    main()
