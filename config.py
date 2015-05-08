class Config():
     CAMERA_SOCKET = '/tmp/camera.socket'
     FFMPEG_BIN = 'ffmpeg'
     FFMPEG_RTMP_OUTPUT = 'rtmp://localhost:25009/webcam/live'
     FFMPEG_PERFRAME_SIZE = 307200
     FFMPEG_FRAME_WIDTH = 640
     FFMPEG_FRAME_HEIGHT = 480
     FFMPEG_COMMAND  = [FFMPEG_BIN,
                        "-f", 'v4l2', '-i','/dev/video0',#'-video_size','%dx%d'%(FFMPEG_FRAME_WIDTH,FFMPEG_FRAME_HEIGHT),
                        '-ac','1','-f','alsa','-i','hw:1',
                        '-ar','22050',
                        '-map','0:0','-map','1:0','-r','15','-f','flv',FFMPEG_RTMP_OUTPUT,
                        '-map','0:0','-f','rawvideo','-r','1','-pix_fmt','gray','unix://'+ CAMERA_SOCKET
                        ]
     DROPBOX_TOKEN = "BsL3s6RgiocAAAAAAAATX7fOo_7xgmVBAADwk1fQtjcAg7gKj8DjsN5aJ61121zX"
     STORAGE_PATH = '/record'