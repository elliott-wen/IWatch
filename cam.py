

import socket
import os
from config import Config
import threading
import numpy as np
import cv2
import logging
import traceback
import cv
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
        conn, addr = self.camera_socket.accept()
        try:
            buffer_t = []
            while self.runFlag:
                data = conn.recv(1024000)
                if(len(data) == 0):
                    logging.info("Client close socket!")
                    break
                buffer_t += data
                while len(buffer_t) >= Config.FFMPEG_PERFRAME_SIZE:
                    clip = buffer_t[:Config.FFMPEG_PERFRAME_SIZE]
                    buffer_t = buffer_t[Config.FFMPEG_PERFRAME_SIZE:]
                    self.process_image(clip)

        except:
            traceback.print_exc()
            self.runFlag = False
            logging.error("Something wrong with the camera socket!")
        logging.info("Camera Thread stops!")

    def process_image(self, data):
        print(len(data))
        img = np.array(data,dtype=np.uint16).reshape((Config.FFMPEG_FRAME_WIDTH,Config.FFMPEG_FRAME_HEIGHT))
        img = cv2.cvtColor(img,cv.CV_YCrCb2BGR)
        cv2.imwrite("/tmp/1.jpg",img)