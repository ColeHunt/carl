"""
Camera.py

Desc: Connection to the camera streaming containers
Author: Isaac Denning
Date: 10/03/23

"""

import docker
import os
import threading

# Which port should be used for each camera.
# The key is the camera ID and the value is the port to stream from.
# To find the camera ID run TODO
STREAM_PORTS = {
    "i77tythguu": 5000,
    "rdkuy5tgrd": 5001
}
IMAGE_NAME = "cysar_camera_streamer"


class CameraStreams:
    """
    Manages Docker containers for streaming video via mjpeg-streamer.

    Args:
        stream_ports (dict): dict of the Camera ID to port. For example,
            {TODO: 5000, TODO: 5001}
        keep_alive (bool): whether the camera stream containers 
            should be rebooted if they stop working 'True' for
            reboot the containter and keep the streams alive
    """
    def __init__(self, stream_ports : dict = STREAM_PORTS, keep_alive : bool = True) -> None:
        self.keep_alive = keep_alive
        self.client = docker.from_env()
        self.image_name = IMAGE_NAME
        self.build_path = os.path.dirname(__file__)
        self.docker_file_path = os.path.join(self.build_path, "Dockerfile")
        self.container = None
        self.keep_alive_thread = None
        self.image = self._get_image()

    
    def _get_image(self, build_if_needed : bool = True) -> docker.models.images.Image:
        """
        Return the Docker image.

        Args:
            build_if_needed (bool): Build the image if non-existent
        """
        if not build_if_needed:
            return self.client.images.get(self.image_name)

        try:
            return self.client.images.get(self.image_name)
        except:
            return self._build_image()

    def _build_image(self) -> docker.models.images.Image:
        """
        Return the builds the Docker image.
        """
        return self.client.images.build(path=self.build_path, dockerfile=self.docker_file_path, quiet=False, rm=True, tag=self.image_name)
    
    def startup(self) -> None:
        """
        Starts the camera streams and initializes keep alive
        threads if that was enabled in constructor.

        TODO
        """
        self.container = self.client.containers.run(image=self.image.id, detach=True)
        if self.keep_alive:
            self.keep_alive_thread = threading.Thread(target=self._keep_stream_alive, args=(self.container, ))
            self.keep_alive_thread.daemon = True
            self.keep_alive_thread.start()
        
    def shutdown(self) -> None:
        """
        Stop all the camera streams.

        TODO
        """
        if self.keep_alive_thread is threading.Thread:
            self.keep_alive = False
            self.keep_alive_thread.join()

        try:
            self.container.stop()
            self.container.remove()
        except: pass

    def get_cameras(self) -> list:
        """
        TODO
        """
        return ["/dev/video0", "/dev/video1"]

    def _keep_stream_alive(self, container : docker.models.containers.Container) -> None:
        """
        TODO
        """
        ACCEPTABLE_STATUS = ["created", "running"]
        while self.keep_alive:
            try:
                container.reload()
            except: pass
            if container.status not in ACCEPTABLE_STATUS:
                try:
                    self.container.remove()
                except: pass
                self.container = self.client.containers.run(image=self.image.id, detach=True)

    def prune_containers(self):
        """
        Removes all containers that were created via this image
        """
        containers = self.client.containers.list(all=True)
        for container in containers:
            if container.attrs['Image'] == self.image.id:
                container.remove(force=True)
    

if __name__ == "__main__":
    cameras = CameraStreams()
    #cameras.startup()
    #cameras.shutdown()
    cameras.prune_containers()