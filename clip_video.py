from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import concatenate_audioclips
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip
import time 
import os
import sys
import csv
import pandas
import threading
import datetime
import re

s_time = time.time()
tz = datetime.timezone(datetime.timedelta(hours=8)) 
now = datetime.datetime.now(tz)  
datatime_str = now.strftime('%Y-%m-%d %H:%M:%S')  
logo = ImageClip("/home/sportvision/highlight_code/logo5.png")
ano_logo = ImageClip("/home/sportvision/highlight_code/ano_logo.png")

# if len(sys.argv) < 3:
#     print("Usage: python script.py input_file.csv input_video.mp4")
#     exit()

if len(sys.argv) < 2:
    print("Usage: python script.py input_file.csv")
    exit()

inn = sys.argv[0]
input_csv_name = sys.argv[1]
# input_video_name = sys.argv[2]
# input_video_name = '2023_compress.mp4'

print(input_csv_name)
# with open(input_csv_name) as f:
#     reader = csv.reader(f)
#     input_data = list(reader)

# print(inn, input_csv_name, input_video_name)

current_path = '/home/sportvision/highlight_code/'

# current_path = os.getcwd()
# output_folder = os.path.join(current_path, 'output/hardcore_clip/')
output_folder = os.path.join(current_path, 'output/clip_video/')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
print(output_folder)

name, _ = input_csv_name.split('.')
cam, year, date_time = name.split('_')
hour, minute, second = date_time.split('-')
video_name = 'v' + str(int(hour)) + '-' + minute 
print(video_name)
csv_path = os.path.join(current_path, 'output/moment_csv/')
input_filepath = os.path.join(csv_path, input_csv_name)



input_video = name + '.mp4'
video_path = os.path.join(current_path, 'output/origin_video/')
input_video_name = os.path.join(video_path, input_video)

input_audio = name + '.wav'
audio_path = os.path.join(current_path, 'output/origin_video/')
input_audio_name = os.path.join(audio_path, input_audio)


input_side_video_2 = 'cam2' + '_' + year + '_' + date_time + '.mp4'
input_side_video_3 = 'cam3' + '_' + year + '_' + date_time + '.mp4'
input_side_video_name_2 = os.path.join(video_path, input_side_video_2)
input_side_video_name_3 = os.path.join(video_path, input_side_video_3)


# id = 0
# with open(input_filepath, 'r') as f:
#     for line in f:
#         diff, start, end = line.strip().split(',')
#         start_time = '00:' + start
#         end_time = '00:' + end
#         print("start time", start_time, end_time)
#         clip = VideoFileClip(input_video_name).subclip(start_time, end_time)
#         clip_name = output_folder + f"{name}_({id}).mp4"
#         clip.write_videofile(clip_name)
#         id += 1


# # 定义处理视频剪辑的函数
# def process_clip(start_time, end_time, input_video_name, input_audio_name, output_folder, clip_name):
#     video_clip = VideoFileClip(input_video_name).subclip(start_time, end_time)
#     audio_clip = AudioFileClip(input_audio_name).subclip(start_time, end_time)
#     final_clip = concatenate_videoclips([video_clip.set_audio(audio_clip)])
#     final_clip.write_videofile(clip_name, threads=4)

def process_clip(before_start_time, start_time, before_end_time, end_time, after_end_time, input_video_name, input_side_video_name, output_folder, input_audio_name, clip_name):
    video_clip = []
    audio_clip = []
    video_clip.append(VideoFileClip(input_side_video_name).subclip(before_start_time, start_time))
    video_clip.append(VideoFileClip(input_video_name).subclip(start_time, end_time))
    video_clip.append(VideoFileClip(input_side_video_name).subclip(before_end_time, after_end_time))
    audio_clip.append(AudioFileClip(input_audio_name).subclip(before_start_time, end_time))
    audio_clip.append(AudioFileClip(input_audio_name).subclip(before_end_time, after_end_time))
    final_audio = concatenate_audioclips(audio_clip)
    # video_clip.write_videofile(clip_name, threads=4)
    final_clip = concatenate_videoclips(video_clip)
    final_clip = concatenate_videoclips([final_clip.set_audio(final_audio)])
    global logo
    logo = logo.set_position((0.045,0.03), relative=True).set_duration(final_clip.duration)
    final_clip = CompositeVideoClip([final_clip, logo])
    global ano_logo
    ano_logo = ano_logo.set_position((0.865,0.03), relative=True).set_duration(final_clip.duration)
    final_clip = CompositeVideoClip([final_clip, ano_logo])
    final_clip.write_videofile(clip_name, threads=10, audio_codec='aac')


# 读取CSV文件
with open(input_filepath, 'r') as f:
    input_data = list(csv.reader(f))

# 处理视频剪辑
id = 0
threads = []
for row in input_data:
    diff, start, end, changeCamTime, t_change_start, start_cam, t_change_end, end_cam, _  = row
    before_start_time = '00:' + t_change_start
    start_time = '00:' + start
    print('before_end_time :', t_change_end )
    h1, m1, s1 = t_change_end.split(':')
    before_end_time = '00:' + t_change_end
    end_time = '00:' + end

    h1 = int(h1)
    m1 = int(m1)
    s1 = float(s1[:len(s1) - len(s1.split('.')[1]) + 7])
    time1 = h1*3600 + m1*60 + s1
    changeCamTime = 6
    t_change_cam = time1 + changeCamTime
    change_hours = int(t_change_cam // 3600)
    change_minutes = int((t_change_cam % 3600) // 60) 
    change_seconds = int(t_change_cam % 60)
    hc = format(change_hours, '02')
    mc = format(change_minutes, '02')
    sc = format(change_seconds, '02.2f')
    after_end_time = f'{hc}:{mc}:{sc}'

    # clip_name = output_folder + f"{name}_({id}).mp4"
    print('time ', before_start_time, start_time, end_time)
    # minutes = re.search(r'\d{2}', video_name).group()
    head, minutes = video_name.split('-')
    print(minutes)
    minutes = int(minutes)
    minutes += id
    if minutes < 10 :
        minutes = "0" + str(minutes)
    # if minutes == 60:
    #     minutes = str(minutes-2)
    new_video_name = head + '-' + str(minutes)
    clip_name = output_folder + f"{new_video_name}.MP4"

    # 新改内容
    # new_video_name = head + '-' + str(minutes)
    # clip_name = output_folder + f"{new_video_name}_{id}.MP4"
    id += 1

    # 判断摄像头

    # t = threading.Thread(target=process_clip, args=(start_time, end_time, input_video_name, input_audio_name, output_folder, clip_name))
    # t = threading.Thread(target=process_clip, args=(start_time, end_time, input_video_name, output_folder, clip_name))
    print('start_cam', type(start_cam))
    if start_cam == '2':
        t = threading.Thread(target=process_clip, args=(before_start_time, start_time, before_end_time, end_time, after_end_time, input_video_name, input_side_video_name_2, output_folder, input_audio_name, clip_name))
    elif start_cam == '3':
        t = threading.Thread(target=process_clip, args=(before_start_time, start_time, before_end_time, end_time, after_end_time, input_video_name, input_side_video_name_3, output_folder, input_audio_name, clip_name))


    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()


e_time = time.time()
print('clip time is ', e_time-s_time )
tz = datetime.timezone(datetime.timedelta(hours=8)) 
now = datetime.datetime.now(tz)  
end_datatime_str = now.strftime('%Y-%m-%d %H:%M:%S')  

with open('clip_time.txt', 'a') as f:
    new_string = datatime_str + ',' + str(e_time-s_time) + ',' +  end_datatime_str + '\n'
    f.write(new_string + '\n')
