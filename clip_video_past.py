from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
import time 
import os
import sys
import csv
import pandas
import threading
import datetime


s_time = time.time()
tz = datetime.timezone(datetime.timedelta(hours=8)) 
now = datetime.datetime.now(tz)  
datatime_str = now.strftime('%Y-%m-%d %H:%M:%S')  


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

current_path = os.getcwd()
output_folder = os.path.join(current_path, 'output/clip_video/')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
print(output_folder)

name, _ = input_csv_name.split('.')

csv_path = os.path.join(current_path, 'output/moment_csv/')
input_filepath = os.path.join(csv_path, input_csv_name)

input_video = name + '.mp4'
video_path = os.path.join(current_path, 'output/origin_video/')
input_video_name = os.path.join(video_path, input_video)

input_audio = name + '.wav'
audio_path = os.path.join(current_path, 'output/origin_video/')
input_audio_name = os.path.join(audio_path, input_audio)


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


# 定义处理视频剪辑的函数
# def process_clip(start_time, end_time, input_video_name, input_audio_name, output_folder, clip_name):
#     video_clip = VideoFileClip(input_video_name).subclip(start_time, end_time)
#     audio_clip = AudioFileClip(input_audio_name).subclip(start_time, end_time)
#     final_clip = concatenate_videoclips([video_clip.set_audio(audio_clip)])
#     final_clip.write_videofile(clip_name, threads=4)

def process_clip(start_time, end_time, input_video_name, output_folder, clip_name):
    video_clip = VideoFileClip(input_video_name).subclip(start_time, end_time)
    video_clip.write_videofile(clip_name, threads=4)


# 读取CSV文件
with open(input_filepath, 'r') as f:
    input_data = list(csv.reader(f))

# 处理视频剪辑
id = 0
threads = []
for row in input_data:
    diff, start, end = row
    start_time = '00:' + start
    end_time = '00:' + end
    clip_name = output_folder + f"{name}_({id}).mp4"
    id += 1
    # t = threading.Thread(target=process_clip, args=(start_time, end_time, input_video_name, input_audio_name, output_folder, clip_name))
    t = threading.Thread(target=process_clip, args=(start_time, end_time, input_video_name, output_folder, clip_name))
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


# import pandas as pd

# # 读取现有 xlsx 文件
# df = pd.read_excel('all_data.xlsx', sheet_name='Sheet1', engine='openpyxl', index_col=0)

# time_tuple = time.gmtime(time.time())
# datatime_str = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)

# # 创建写入的数据
# new_data = pd.Series(['this is clipvideo time ' + str(e_time-s_time) + '|' +  datatime_str])

# # 添加新的行
# df['row'] = df['row'].append(new_data)

# # 写出到 xlsx 文件
# df.to_excel('all_data.xlsx', sheet_name='Sheet1')  



# import openpyxl
# workbook = openpyxl.load_workbook('all_data.xlsx')
# workbook = workbook.active
# time_tuple = time.gmtime(time.time())
# datatime_str = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)
# workbook.append(['this is clipvideo time ',str(e_time-s_time), datatime_str])

# workbook.save('all_data.xlsx')

# with open('all_data.x', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerows('this is clipvideo time '+str(e_time-s_time) )
#     writer.writerows(time.gmtime())
