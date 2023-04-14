#!/bin/sh

# Input should be a single line from lsusb output:
DATA=`lsusb | grep "CAN adapter"`

# Read the bus number:
BUS=`echo $DATA | grep -Po 'Bus 0*\K[1-9]+'`

# Read the device number:
DEV=`echo $DATA | grep -Po 'Device 0*\K[1-9]+'`

BUS_FILL=`printf '%03d\n' "$BUS"`
DEV_FILL=`printf '%03d\n' "$DEV"`

PATH=/dev/bus/usb/$BUS_FILL/$DEV_FILL

/usr/bin/slcand -o -c -s0 $PATH can0
/usr/bin/ip link set can0 type can bitrate 1000000
/usr/sbin/ifconfig can0 up
/usr/sbin/ifconfig can0 txqueuelen 1000
