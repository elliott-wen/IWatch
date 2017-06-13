from cam import CameraMotionDetector
from ffmpeg import FFMPEG_Watchdog
import logging
import time
import os
# from storage import DropboxStorage
def main():
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s')
    cam = CameraMotionDetector()
    cam.open_camera()
    watchdog = FFMPEG_Watchdog()
    watchdog.kill_ffmpeg()
    watchdog.start_ffmpeg()
    
    try:
        watchdog.join();
    except:
        pass
    finally:
        watchdog.kill_ffmpeg()
        cam.stop_camera()
        # store.stop_uploader()
        logging.info("Ready to shutdown!")
        # time.sleep(10)
        os._exit(-1)

if __name__ == '__main__':
    main()
