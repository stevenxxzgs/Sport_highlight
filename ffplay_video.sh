#!/bin/bash

dir_path="output/clip_video"
file_ext="MP4"
VIDEO_FOLDER="/home/sportvision/highlight_code/output/clip_video"
VIDEO_LIST="/home/sportvision/highlight_code/video_list.txt"

# ffplay -fs -nostats -hide_banner -autoexit "output/clip_video/v17-25.MP4" &> /dev/null 
feh --fullscreen --fill /home/sportvision/highlight_code/background.jpg &

ls -t "${VIDEO_FOLDER}"/*.MP4 | head -n 5 > "${VIDEO_LIST}" #相对路径
# ls "${VIDEO_FOLDER}"/*.mp4 > "${VIDEO_LIST}"
# ls -t "${VIDEO_FOLDER}"/*.MP4 | head -n 4 | sed 's/^/"/;s/$/"/' > "${VIDEO_LIST}"
# ls -t "${VIDEO_FOLDER}"/*.mp4 | head -n 4 | sed "s|^|$(pwd)/|" > "${VIDEO_LIST}"

a=$(head -n 1 "$VIDEO_LIST")
sed -i '1d' "$VIDEO_LIST"
echo $a >> "$VIDEO_LIST"
echo $a
count=0
# ffplay -autoexit "$a"
check_video_folder() {
  if [[ -n $(find "$VIDEO_FOLDER" -maxdepth 0 -type d -empty 2>/dev/null) ]]; then
    echo "视频文件夹为空"
    sleep 30
    return 1 # 返回非零值表示文件夹为空
  fi
  return 0 # 返回零值表示文件夹不为空
}

play_video() {
  while read -r a; do
    sed -i '1d' "$VIDEO_LIST"
    echo "$a" >> "$VIDEO_LIST"
    ffplay -autoexit -fs "$a"
    sleep 3
    # ((count++))
  done < "$VIDEO_LIST"
}

while true; do
  check_video_folder || sleep 10 # 如果文件夹为空，则等待5秒钟后继续循环

  play_video
  sleep 5
  play_video
  if inotifywait -q -e close_write --format '%f' "${VIDEO_FOLDER}"; then
    play_video
    ls -t "${VIDEO_FOLDER}"/*.MP4 | head -n 4 > "${VIDEO_LIST}" #相对路径
  else 
    sleep 5
  fi
done