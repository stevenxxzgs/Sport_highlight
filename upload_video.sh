VIDEO_FOLDER="/home/sportvision/highlight_code/output/clip_video"
PYTHON_SCRIPT="/home/sportvision/highlight_code/uploader.py"
# uploader_ori 上传取主机位辅码流的origin_video
UPLOADER_ORI_SCRIPT="/home/sportvision/highlight_code/uploader_ori.py"

inotifywait -m -e close_write --format '%f' "${VIDEO_FOLDER}" | while read filename 
do
    if [[ "$filename" == *.mp4 ]] || [[ "$filename" == *.avi ]] || [[ "$filename" == *.MP4 ]]

    then
        # 在终端输出文件名
        echo "New video file detected: ${filename}"
        
        # sudo curl -F "file=@${VIDEO_FOLDER}/${filename}" 118.195.248.204/upload

        python "${PYTHON_SCRIPT}" "${filename}"
        python "${UPLOADER_ORI_SCRIPT}" "${filename}"
    fi
done