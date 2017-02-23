class Config():
     CAMERA_SOCKET = '/tmp/camera.socket'
     FFMPEG_BIN = 'ffmpeg'
     FFMPEG_RTMP_OUTPUT = 'rtmp://a.rtmp.youtube.com/live2/t5ue-24sa-as03-9kra'
     FFMPEG_PERFRAME_SIZE = 307200
     FFMPEG_FRAME_WIDTH = 640
     FFMPEG_FRAME_HEIGHT = 480
     FFMPEG_COMMAND  = [FFMPEG_BIN,
                        "-f", 'v4l2', '-framerate', '15', '-video_size', '640*480',  '-i','/dev/video0',
                        '-ac','1','-f','alsa','-i','hw:1',
                        '-ar','22050',
                        '-map','0:0','-map','1:0','-vcodec','h264_omx', '-g', '30', '-f','flv',FFMPEG_RTMP_OUTPUT,
                        '-map','0:0','-f','rawvideo','-r','1','-pix_fmt','gray','unix://'+ CAMERA_SOCKET
                        ]


     DETECTION_IMAGE = '/tmp/detection.jpg'
     DETECTION_THRESHOLD = 700000
     DETECTION_SENDMESSAGE_INTERVAL = 1800
     DETECTION_SENSITITY = 7

     MAIL_ACCOUNT = "hellomimi55@126.com"
     MAIL_SERVER = "smtp.126.com"
     MAIL_PASSWORD = "huangguiying"
     NOTIFY_MAIL_ACCOUNT = ["jq.elliott.wen@gmail.com", "gy.victoria.huang@gmail.com"]

