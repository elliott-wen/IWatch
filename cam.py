

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
        self.lastImg = None

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
            buffer_t = ""
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
        img = np.frombuffer(data,dtype=np.uint8,count=Config.FFMPEG_FRAME_HEIGHT*Config.FFMPEG_FRAME_WIDTH).reshape((Config.FFMPEG_FRAME_HEIGHT,Config.FFMPEG_FRAME_WIDTH))
        self.detect_motion(img)

    def detect_motion(self,img):
        if not self.lastImg:
            self.lastImg = img
            return False
        diff = cv2.absdiff(self.lastImg,img)
        kernel = np.ones((5,5),np.uint8)
        diff = cv2.medianBlur(diff,5)
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
        diff = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, kernel)
        diff = cv2.threshold(diff,10,255,cv2.THRESH_BINARY)
        print(diff)
        self.lastImg = img
        return False