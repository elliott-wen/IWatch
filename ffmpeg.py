import threading
import os
import logging
import time
import subprocess
from config import Config
class FFMPEG_Watchdog(threading.Thread):

    def __init__(self):
        super(FFMPEG_Watchdog,self).__init__(name="FFMPEG Thread")

    def kill_ffmpeg(self):
        try:
            logging.info("Trying to kill the existing ffmpeg instance!")
            os.system("killall ffmpeg")
            time.sleep(1)
        except:
            pass

    def start_ffmpeg(self):
        self.start()

    def run(self):
        nullFile = open('/dev/null','w')
        logging.info("Starting FFMPEG")
        print(Config.FFMPEG_COMMAND)
        subprocess.call(Config.FFMPEG_COMMAND,stdout=nullFile)
        logging.info("FFMPEG ends!")

