
PYTHON_SCRIPT="/home/sportvision/highlight_code/moment_video.py"
CSV_FOLDER="/home/sportvision/highlight_code/output/sub_video"
inotifywait -m -e close_write --format '%f' "${CSV_FOLDER}" | while read filename 
do
    if [[ "$filename" == *.csv ]] 
    then
        # 在终端输出文件名
        echo "New csv file detected: ${filename}"
        
        # 参数需要有一个文件名，这个文件是算法执行之后的predict文件
        python "${PYTHON_SCRIPT}" "${filename}"
    fi
done
