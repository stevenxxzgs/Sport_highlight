from moviepy.video.VideoClip import ImageClip
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
import time
time.sleep(2)
import sys
import os
# 输入参数需要有一个文件名
if len(sys.argv) < 2:
    print("Usage: python script.py filename")
    exit()
current_path = '/home/sportvision/highlight_code/'

# current_path = os.getcwd()
output_folder = os.path.join(current_path, 'output/record_video/')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


video_name = sys.argv[1]
head, _ = video_name.split('.')
cam, year, date_time = head.split('_')
hour, minute, second = date_time.split('-')
minute = int(minute) + 2
if minute < 10 :
    minute = "0" + str(minute)
if minute == 60 or minute == 61 or minute == 62:
    minute = str(minute-3)
out_video_name = 'v' + str(int(hour)) + '-' + str(minute) + '.MP4' # 文件名后面添个零，表示origin record
print(out_video_name)
audio_name = head + '.wav'
audio_path = os.path.join(current_path, 'output/origin_video/')
input_audio_name = os.path.join(audio_path, audio_name)

video_path = os.path.join(current_path, 'output/origin_video/')
input_video_name = os.path.join(video_path, video_name)

output_video = output_folder + out_video_name

# video_clip = VideoFileClip(input_video_name)
# audio_clip = AudioFileClip(input_audio_name)

# final_clip = concatenate_videoclips([video_clip.set_audio(audio_clip)])
# # logo = ImageClip('logo5.png')
# # logo = logo.set_position((0.045,0.03), relative=True).set_duration(final_clip.duration)
# # final_clip = CompositeVideoClip([final_clip, logo])
# final_clip.write_videofile(out_video_name, threads=4)

import subprocess

output_file = output_video
cmd = f"ffmpeg -i {input_video_name} -i {input_audio_name} -c:v copy -c:a aac -strict experimental {output_file}"
subprocess.run(cmd, shell=True)