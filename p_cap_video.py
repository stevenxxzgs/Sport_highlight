import threading
import time
import subprocess
import datetime


def run_script(filename1, filename2, filename3, filename4, filename5):
    # 调用 .py
    print(filename1, filename2, filename3, filename4, filename5)
    subprocess.Popen(["python", "/home/sportvision/highlight_code/get_sub_video.py", filename1])
    subprocess.Popen(["python", "/home/sportvision/highlight_code/audio_ffmpeg.py", filename5]) 
    # subprocess.Popen(["python", "/home/sportvision/highlight_code/cam1.py", filename1])
    subprocess.Popen(["python", "/home/sportvision/highlight_code/cam2.py", filename2])
    subprocess.Popen(["python", "/home/sportvision/highlight_code/cam3.py", filename3])
    subprocess.Popen(["python", "/home/sportvision/highlight_code/cam_origin_ffmpeg.py", filename1])

if __name__ == '__main__':
    # 每 5 min 运行一次
    interval = 300
    while True:
        now = datetime.datetime.now()
        morning = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=8, minute=30)
        night = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=22, minute=10)
        # 将日期和时间格式化为字符串
        time_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        if now > morning and now < night :
            # 将时间戳添加到文件名中
            filename1 = f"cam1_{time_string}.mp4"
            filename2 = f"cam2_{time_string}.mp4"
            filename3 = f"cam3_{time_string}.mp4"
            filename4 = f"cam4_{time_string}.mp4"
            filename5 = f"cam1_{time_string}.wav"
            thread = threading.Thread(target=run_script, args=(filename1, filename2, filename3, filename4, filename5))
            thread.start()
            time.sleep(interval)
        else:
            print('not the time')
            time.sleep(interval)