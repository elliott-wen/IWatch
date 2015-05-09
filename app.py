from cam import Camera
from ffmpeg import FFMPEG_Watchdog
import logging
import time
import os
from storage import DropboxStorage
def main():
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s')
    cam = Camera()
    cam.open_camera()
    watchdog = FFMPEG_Watchdog()
    watchdog.kill_ffmpeg()
    watchdog.start_ffmpeg()
    store = DropboxStorage()
    store.start_uploader()
    time.sleep(1)
    runFlag = True
    try:
        while runFlag:
            time.sleep(1)
            if(cam.isAlive() == False or watchdog.isAlive() == False):
                break
    except:
        pass
    finally:
        watchdog.kill_ffmpeg()
        cam.stop_camera()
        store.stop_uploader()
        logging.info("Ready to shutdown!")
        time.sleep(10)
        os._exit(-1)

if __name__ == '__main__':
    main()