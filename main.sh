#!/bin/bash

nohup bash /home/sportvision/highlight_code/moment_video.sh &> /home/sportvision/highlight_code/moment_video.log &
nohup bash /home/sportvision/highlight_code/algorithm.sh &> /home/sportvision/highlight_code/algorithm.log &
nohup bash /home/sportvision/highlight_code/clip_video.sh &> /home/sportvision/highlight_code/clip_video.log &
nohup bash /home/sportvision/highlight_code/record_video.sh &> /home/sportvision/highlight_code/record_video.log &
nohup bash /home/sportvision/highlight_code/upload_video.sh &> /home/sportvision/highlight_code/upload_video.log &
# nohup bash /home/sportvision/highlight_code/modify_alg.sh
#    nohup bash video_play.sh & 
