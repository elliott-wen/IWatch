

import socket
import os
from config import Config
import threading
import logging
class Camera(threading.Thread):


    def __init__(self):
        super(Camera,self).__init__(name="Camera Thread")
        self.camera_socket = None
        self.runFlag = False

    def open_camera(self):
        self.camera_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove(Config.CAMERA_SOCKET)
        except OSError:
            pass
        self.camera_socket.bind(Config.CAMERA_SOCKET)
        self.camera_socket.listen(1)
        self.runFlag = True
        self.start()

    def stop_camera(self):
        self.runFlag = False

    def run(self):
        conn = self.camera_socket.accept()
        while(self.runFlag):
            try:
                data = conn.recv(10240)
                print(len(data))
            except:
                self.runFlag = False
                logging.error("Something wrong with the camera socket!")
        logging.info("Camera Thread stops!")
