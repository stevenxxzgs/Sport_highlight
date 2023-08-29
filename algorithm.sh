# #!/bin/bash

# # 设置视频文件夹的路径
# VIDEO_FOLDER="/home/sportvision/SportVision/Detect/3_in_3_out/output"

# # 设置 Python 脚本的路径
# PYTHON_SCRIPT="/home/sportvision/SportVision/Detect/3_in_3_out/hello.py"

# # 监听视频文件夹中是否有新的文件写入完成
# inotifywait -m -e close_write --format '%f' "${VIDEO_FOLDER}" | while read filename
# do
#     # 检查文件扩展名是否为 .mp4 或 .avi
#     if [[ "$filename" == *.mp4 ]] || [[ "$filename" == *.avi ]]
#     then
#         # 在终端输出文件名
#         echo "New video file detected: ${filename}"
        
#         # 运行 Python 脚本并传递文件名作为参数
#         python "${PYTHON_SCRIPT}" "${VIDEO_FOLDER}/${filename}"
#     fi

#     # if  [[ "$filename" == *.csv ]] 
#     # then
#     #     python

#     # fi
# done



#!/bin/bash

# 设置视频文件夹的路径
VIDEO_FOLDER="/home/sportvision/highlight_code/output/sub_video"
PYTHON_SCRIPT="/home/sportvision/highlight_code/predict3.py"

# 监听视频文件夹中是否有新的文件写入完成
inotifywait -m -e close_write --format '%f' "${VIDEO_FOLDER}" | while read filename 
do
    # 检查文件扩展名是否为 .mp4 或 .avi
    if [[ "$filename" == *.mp4 ]] || [[ "$filename" == *.avi ]]
    then
        # 在终端输出文件名
        echo "New video file detected: ${filename}"
        
        python "${PYTHON_SCRIPT}" "--video_name=${VIDEO_FOLDER}/${filename}" "--load_weights=/home/sportvision/highlight_code/newmodel.h5"
    fi
done