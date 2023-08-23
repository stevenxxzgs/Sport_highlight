# import glob
# import subprocess

# for filename in glob.glob("*.mp4"):
#     print(f"处理文件:{filename}")
#     # subprocess.Popen(["python", "s.py", filename])


import argparse
import os
import subprocess

input_dir = os.getcwd()
input_dir = os.path.join(input_dir, 'output/sub_video')

csv_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]

for csv_file in csv_files:
    # csv_file = os.path.splitext(mp4_file)[0] + ".csv"
    # mp4_path = os.path.join(input_dir, mp4_file)
    # csv_path = os.path.join(input_dir, csv_file)
    # print(f"处理文件: {csv_file}")
    subprocess.Popen(["python", "moment_video.py", csv_file])