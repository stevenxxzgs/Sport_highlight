import cv2
import time
import datetime
import os

# 获取当前日期和时间
tz = datetime.timezone(datetime.timedelta(hours=8)) 
now = datetime.datetime.now(tz)
datatime_str = now.strftime('%Y-%m-%d %H:%M:%S')


import sys
# 输入参数需要有一个文件名
if len(sys.argv) < 2:
    print("Usage: python script.py filename")
    exit()

filename1 = sys.argv[1]

# 将时间戳添加到文件名中
# filename1 = f"cam1_{time_string}.mp4"

path = "/home/sportvision/highlight_code/output/sub_video"

# 创建output文件夹（如果不存在）
if not os.path.exists(path):
    os.makedirs(path)

# 创建完整的文件路径
filepath1 = os.path.join(path, filename1)

start = time.time()

# 辅码流
capture = cv2.VideoCapture("rtsp://admin:xu123456@192.168.1.251:554/cam/realmonitor?channel=1&subtype=1")
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(capture.get(cv2.CAP_PROP_FPS))
new_width = 640
new_height = 360
fourcc1 = cv2.VideoWriter_fourcc(*"XVID")
out1 = cv2.VideoWriter(filepath1, fourcc1, fps, (370, 310))


i = 0
while True:
    # s = time.time()
    ret, frame = capture.read()
    # e = time.time()
    # print("this is cap time ", e-s)
    # s = time.time()
    if ret:
        resized_frame = cv2.resize(frame, (new_width, new_height))
        # print(resized_frame.shape)
        cropped_frame = resized_frame[:310, 87:457, :]

        out1.write(cropped_frame)

    # e = time.time()
    # print("this is write time ", e-s)
    del(ret)
    del(frame)
    i += 1
    if i > fps*300:
        break

out1.release()
capture.release()

end = time.time()
print("time is", end-start)
time_tuple = time.gmtime(time.time())
end_datatime_str = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)


with open('sub_time.txt', 'a') as f:
    new_string = datatime_str + ',' + str(end-start) + ',' + end_datatime_str +'\n'
    f.write(new_string)