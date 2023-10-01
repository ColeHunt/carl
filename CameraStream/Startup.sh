#!/bin/sh

USER=`whoami`
if [ $USER != "root" ]; then
	echo "Must be run as root! (sudo ./Startup.sh)"
	exit
fi

# Try to remove the container if it already exists
docker rm -f camera_server 2>/dev/null

DOCKER_CMD="docker run"
CAMERA_COUNT=`ls /dev/video* | wc -l`

# Loop through video devices
for i in $(seq 0 1 $CAMERA_COUNT); do
  VIDEO_DEVICE="/dev/video$i"
  
  # Check if the video device exists
  if [ -e "$VIDEO_DEVICE" ]; then
    # Add device and port mapping to the Docker command
    DOCKER_CMD="$DOCKER_CMD --device=$VIDEO_DEVICE -p $((5000 + i)):$((5000 + i))"
  fi
done

# Add the image to the Docker command
DOCKER_CMD="$DOCKER_CMD -d --name camera_server camera_server"

echo $DOCKER_CMD

# Run docker
eval "$DOCKER_CMD"