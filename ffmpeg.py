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
        command = [Config.FFMPEG_BIN,
                        "-f", 'v4l2', '-i','/dev/video0',
                        '-ac','1','-f','alsa','-i','hw:1',
                        '-ar','22050','-map','0:0','-map','1:0',
                        '-r','15','-f','flv',Config.FFMPEG_RTMP_OUTPUT,
                        '-map','0:0','-f','rawvideo','-r','1','unix://'+Config.CAMERA_SOCKET
                        ]

        logging.info("Starting FFMPEG")

        subprocess.call(command)
        logging.info("FFMPEG ends!")

