import cv2
import time
from threading import Thread
# from multiprocessing import Process
from collections import deque
import datetime
import os
import numpy as np
import sys
s = time.time()

# # 获取当前日期和时间
# now = datetime.datetime.now()
# # 将日期和时间格式化为字符串
# time_string = now.strftime("%Y-%m-%d_%H-%M-%S")
# # 将时间戳添加到文件名中
# filename1 = f"cam2_{time_string}.mp4"

import sys
# 输入参数需要有一个文件名
if len(sys.argv) < 2:
    print("Usage: python script.py filename")
    exit()

filename1 = sys.argv[1]


time_tuple = time.gmtime(time.time())
datatime_str = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)
capture = cv2.VideoCapture("rtsp://admin:xu123456@192.168.1.252:554/cam/realmonitor?channel=1&subtype=0")

def read_frames(capture, frames, recording_time):
    start_time = time.time()
    # count = 1
    while time.time() - start_time < recording_time:
        ret, frame = capture.read()
        if not ret:
            break
        frames.append(frame[:1000, 20:1520, :])
        # print("read count is ", count)
        # count+=1
        if len(frames) > max_frames:
            frames.popleft()
    capture.release()


# def write_frames(out, frames, recording_time):
    # start_time = time.time()
    # while time.time() - start_time < recording_time:
    #     if frames:
    #         frame = frames.popleft()
    #         out.write(frame)


def write_frames(out, frames, recording_time, w, h):
    start_time = time.time()
    # count = 1
    # while time.time() - start_time < recording_time:
    while time.time() - start_time < recording_time or frames:
        if frames:
            frame = frames.popleft()
            # frame = frame[:h,:w,:]
            # print('frame is', type(frame))
            # print('frame shape is ', frame.shape)
            out.write(frame)
            # print("write count is ", count)
            # count+=1
        else:
            time.sleep(0.00001) 
    out.release()

# 设置录制时长
recording_time = 300

path = "/home/sportvision/highlight_code/output/origin_video"


# 创建output文件夹（如果不存在）
if not os.path.exists(path):
    os.makedirs(path)
# 创建完整的文件路径
filepath1 = os.path.join(path, filename1)


# capture = cv2.VideoCapture("rtsp://admin:xu123456@192.168.2.2:554/cam/realmonitor?channel=1&subtype=0")
# width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = 1500
height = 1000
fps = int(capture.get(cv2.CAP_PROP_FPS))
print(fps)
# 设置循环缓冲区最大帧数
max_frames = fps * recording_time

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out1 = cv2.VideoWriter(filepath1, fourcc, fps, (width, height))



frames = deque(maxlen=max_frames)
write_thread = Thread(target=write_frames, args=(out1, frames, recording_time, int(width/2), int(height/2) ))
capture_thread = Thread(target=read_frames, args=(capture, frames, recording_time))
capture_thread.start()  
write_thread.start()


capture_thread.join()
write_thread.join()

# cv2.destroyAllWindows()
e = time.time()
print('time is', e-s)

time_tuple = time.gmtime(time.time())
end_datatime_str = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)


with open('ori_time.txt', 'a') as f:
    new_string = datatime_str + ',' + str(e-s) + ',' + end_datatime_str +'\n'
    f.write(new_string)
