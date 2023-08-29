# clip_csv 会放有剪辑需要的时间戳, 这里使用python moviepy直接剪
CSV_FOLDER="/home/sportvision/highlight_code/output/moment_csv"
PYTHON_SCRIPT="/home/sportvision/highlight_code/clip_video.py"

inotifywait -m -e close_write --format '%f' "${CSV_FOLDER}" | while read filename 
do
    if [[ "$filename" == *.csv ]] 
    then
        # 在终端输出文件名
        echo "New csv file detected: ${filename}"
        # sleep 30
        python "${PYTHON_SCRIPT}" "${filename}"
    fi
done