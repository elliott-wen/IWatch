class Config():
     CAMERA_SOCKET = '/tmp/camera.socket'
     FFMPEG_BIN = 'ffmpeg'
     FFMPEG_RTMP_OUTPUT = 'rtmp://a.rtmp.youtube.com/live2/t5ue-24sa-as03-9kra'
     FFMPEG_PERFRAME_SIZE = 307200
     FFMPEG_FRAME_WIDTH = 640
     FFMPEG_FRAME_HEIGHT = 480
     FFMPEG_COMMAND  = [FFMPEG_BIN,
                        "-f", 'v4l2', '-framerate', '15', '-video_size', '640*480', '-g', '30', '-i','/dev/video0',
                        '-ac','1','-f','alsa','-i','hw:1',
                        '-ar','22050',
                        '-map','0:0','-map','1:0','-vcodec','h264_omx', '-f','flv',FFMPEG_RTMP_OUTPUT,
                        '-map','0:0','-f','rawvideo','-r','1','-pix_fmt','gray','unix://'+ CAMERA_SOCKET
                        ]


     DETECTION_IMAGE = '/tmp/detection.jpg'
     DETECTION_THRESHOLD = 500000
     DETECTION_SENDMESSAGE_INTERVAL = 1800
     DETECTION_SENSITITY = 7
     PUSHOVER_KEY = 'up2yuJNRLij6Gr3YcJK5j0dPVkJsFF2Y'

