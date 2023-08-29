# combine
VIDEO_FOLDER="/home/sportvision/highlight_code/output/origin_video"
PYTHON_SCRIPT="/home/sportvision/highlight_code/record_video.py"

inotifywait -m -e close_write --format '%f' "${VIDEO_FOLDER}" | while read filename 
do
    if [[ "$filename" == *cam1*.mp4 ]] || [[ "$filename" == *cam1*.avi ]] || [[ "$filename" == *cam1*.MP4 ]]

    then
        # 在终端输出文件名
        echo "New video file detected: ${filename}"
        # sudo curl -F "file=@${VIDEO_FOLDER}/${filename}" 118.195.248.204/upload
        python "${PYTHON_SCRIPT}" "${filename}"
    fi
done