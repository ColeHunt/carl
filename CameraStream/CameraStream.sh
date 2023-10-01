#!/bin/sh

# Find how many cameras are connected
CAMERA_COUNT=`ls /dev/video* | wc -l`
echo "Number of cameras $CAMERA_COUNT"

# For each camera startup a seperate stream on port 5000, 5001, 5002...
#    Can be accessed via http://<jetson-ip>:<camera-port>/?action=stream
for i in $(seq 0 1 $(($CAMERA_COUNT-1)))
do
        mjpg_streamer -i "input_uvc.so -d /dev/video$i" -o "output_http.so -p $(($i+5000))" &
done


sleep infinity