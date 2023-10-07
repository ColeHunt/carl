#!/usr/bin/python3

"""
Camera.py

Desc: Connection to the camera streaming containers
Author: Isaac Denning
Date: 10/03/23

"""

import docker
import os
import threading
import subprocess

# Which port should be used for each camera.
# The key is the camera ID and the value is the port to stream from.
# To find the camera ID run "ls -l /dev/v4l/by-id/"
DEFAULT_STREAM_PORTS = [
    {
        "Cam_UUID": "/dev/v4l/by-id/usb-H264_USB_Camera_H264_USB_Camera_2020032801-video-index0",
        "Port": 5000
    }
]

DEFAULT_IMAGE_NAME = "cysar_camera_streamer"
DEFAULT_DOCKER_PATH = os.path.dirname(__file__)

class CameraStream:
    """
    Manages Docker containers for streaming video via mjpeg-streamer.

    Args:
        stream_ports (list): list of the Camera ID and port. For example,
            [{"Cam_UUID": usb-Camera-video-index0, "Port": 5000}]
        build_path (str): The path to the Dockerfile
    """
    def __init__(self, stream_ports : dict = DEFAULT_STREAM_PORTS,
                 docker_path : str = DEFAULT_DOCKER_PATH
                 ) -> None:
        self.stream_ports = stream_ports
        self.image_name = DEFAULT_IMAGE_NAME
        self.docker_path = docker_path
        self._client = docker.from_env()
        self._image = self._get_image()
        self._containers = []
        self._host_threads = []
        self._run_threads = False

    def _get_image(self, build_if_needed : bool = True) -> docker.models.images.Image:
        """
        Return the Docker image.

        Args:
            build_if_needed (bool): Build the image if non-existent
        """
        if not build_if_needed:
            return self._client.images.get(self.image_name)

        try:
            return self._client.images.get(self.image_name)
        except:
            return self._build_image()

    def _build_image(self) -> docker.models.images.Image:
        """
        Return the builds the Docker image.
        """
        self._client.images.build(path=self.docker_path,
                                 dockerfile="Dockerfile",
                                 quiet=False,
                                 rm=True,
                                 tag=self.image_name)
        return self._client.images.get(self.image_name)

    def _host_stream(self, CameraID : str, port : int) -> None:
        """
        TODO
        """
        container = None
        while self._run_threads:
            camera = [cam[1] for cam in self.get_cameras() if cam[0] == CameraID]
            print(self.get_cameras(), CameraID)
            if camera: # If the camera with ID exists
                camera = camera[0] # Should only be one match anyways
                self._client.containers.run(image=self._image.id,
                                           detach=True,
                                           devices=[camera+":/dev/video0:rwm"],
                                           ports={'5000/tcp': port})
                input("Wait a minute")
            else:
                pass

    def startup(self) -> None:
        """
        TODO
        """
        self._run_threads = True
        for stream in self.stream_ports:
            thread = threading.Thread(target=self._host_stream, args=(stream["Cam_UUID"], stream["Port"]))
            self._host_threads += [thread]
            thread.start()

    def shutdown(self) -> None:
        """
        Stop all the camera streams.
        TODO
        """
        pass

    def get_cameras(self) -> list:
        """
        Returns the cameras currently connected to the system.
        index 0 is a unique identifier and index 1 is the device.

        Example:
            [
                ['/dev/v4l/by-id/usb-H264_USB_Camera_H264_USB_Camera_2020032801-video-index0', '/dev/video0'],
                ['/dev/v4l/by-id/usb-H264_USB_Camera_H264_USB_Camera_2020032801-video-index1', '/dev/video1']
            ]
        """
        cmd = "ls -ld /dev/v4l/by-id/* | tr -s \" \" | awk -F ' ' '{print $9,$11}'"
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0].decode('UTF-8')
        cameras = output.strip().split('\n')
        cameras = [cam.split(' ') for cam in cameras]
        cameras = [[cam[0], "/dev/v4l/by-id/"+cam[1]] for cam in cameras]
        return cameras

    def prune_containers(self):
        """
        Removes all containers that were created via this image
        """
        containers = self._client.containers.list(all=True)
        for container in containers:
            if container.attrs['Image'] == self._image.id:
                container.remove(force=True)

if __name__ == "__main__":
    cameras = CameraStream()
    cameras.get_cameras()
    #cameras.startup()
    #cameras.shutdown()
    cameras.prune_containers()
