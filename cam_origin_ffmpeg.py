import subprocess as sp
import cv2
import numpy as np
import time
import os
start_time = time.time()
# 设置rtsp URL
rtsp_url = "rtsp://admin:xu123456@192.168.1.251:554/cam/realmonitor?channel=1&subtype=2"

# 设置录制时长
recording_time = 300
logo_file = '/home/sportvision/highlight_code/logo5.png'
# # 设置输出路径和文件名, .wav只保留音频文件
output_path = "/home/sportvision/highlight_code/output/origin_video"

# now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
# # filename = f"cam1_{now}.wav"
# filename = f'cam1_{now}.mp4'

import sys
# 输入参数需要有一个文件名
if len(sys.argv) < 2:
    print("Usage: python script.py filename")
    exit()

filename = sys.argv[1]

output_file = os.path.join(output_path, filename)

# 设置ffmpeg命令行参数, -vn -acodec pcm_s16le
ffmpeg_cmd = ['ffmpeg',
              '-rtsp_transport',  'tcp',
              '-i', rtsp_url,
              '-i', logo_file,
              '-filter_complex', '[0:v]crop=1500:1000:60:0[v];[v][1:v]overlay=67.5:30',
              '-c:v', 'libx264',
              '-crf', '23',
              '-preset', 'veryfast',
              '-t', str(recording_time),
              '-c:a', 'aac',
              '-strict', 'experimental',
              output_file]

# ffmpeg -rtsp_transport tcp -i rtsp://<IP_ADDRESS>:<PORT>/<STREAM_PATH> -f alsa -i hw:0 -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -strict experimental output.mp4

p = sp.Popen(ffmpeg_cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
# 等待进程结束
output, error = p.communicate()
if p.returncode != 0:
    print(f"Error occurred: {error.decode('utf-8')}")
else:
    print(f"Video saved to {output_file}")

end_time = time.time()
print('get_video time is ', end_time-start_time)