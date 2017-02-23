import threading
import os
import logging
import time
import subprocess32
from config import Config
class FFMPEG_Watchdog(threading.Thread):

    def __init__(self):
        super(FFMPEG_Watchdog,self).__init__(name="FFMPEG Thread")
        runningFlag = True

    def kill_ffmpeg(self):
        try:
            self.runningFlag = False
            logging.info("Trying to kill the existing ffmpeg instance!")
            os.system("killall ffmpeg")
            time.sleep(1)
        except:
            pass

    def start_ffmpeg(self):
        self.runningFlag = True
        self.start()

    def run(self):
        nullFile = open('/dev/null','w')
        #logging.info("Starting FFMPEG")

        while self.runningFlag:
            logging.info("Start up FFmpeg %s"%Config.FFMPEG_COMMAND)
            subprocess32.call(Config.FFMPEG_COMMAND,stdout=nullFile,stderr=nullFile)
            logging.info("FFMPEG ends! Try Start it in 10 Sec")
            time.sleep(10)

