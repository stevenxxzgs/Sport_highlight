import sys
import getopt
import numpy as np
import os
from glob import glob
import piexif
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import *
from keras.layers import *
from TrackNet3 import TrackNet3
import keras.backend as K
from keras import optimizers
import tensorflow as tf
import cv2
from os.path import isfile, join
from PIL import Image
import time
import csv
import datetime
BATCH_SIZE=1
HEIGHT=288
WIDTH=512
# HEIGHT=360
# WIDTH=640
sigma=2.5
mag=1

start = time.time()
tz = datetime.timezone(datetime.timedelta(hours=8)) 
now = datetime.datetime.now(tz)  
datatime_str = now.strftime('%Y-%m-%d %H:%M:%S')  


def genHeatMap(w, h, cx, cy, r, mag):
	if cx < 0 or cy < 0:
		return np.zeros((h, w))
	x, y = np.meshgrid(np.linspace(1, w, w), np.linspace(1, h, h))
	heatmap = ((y - (cy + 1))**2) + ((x - (cx + 1))**2)
	heatmap[heatmap <= r**2] = 1
	heatmap[heatmap > r**2] = 0
	return heatmap*mag

# 时间,微秒: in milliseconds
def custom_time(time):
	remain = int(time / 1000)
	ms = (time / 1000) - remain
	s = remain % 60
	s += ms
	remain = int(remain / 60)
	m = remain % 60
	remain = int(remain / 60)
	h = remain
	#生成自定义的时间str
	cts = ''
	if len(str(h)) >= 2:
		cts += str(h)
	else:
		for i in range(2 - len(str(h))):
			cts += '0'
		cts += str(h)
	
	cts += ':'

	if len(str(m)) >= 2:
		cts += str(m)
	else:
		for i in range(2 - len(str(m))):
			cts += '0'
		cts += str(m)

	cts += ':'

	if len(str(int(s))) == 1:
		cts += '0'
	cts += str(s)

	return cts


# def custom_time(time):
#     # 计算小时、分钟和秒数
#     h, rem = divmod(int(time) // 1000, 3600)
#     m, s = divmod(rem // 60, 60)
#     # 生成自定义时间字符串
#     return f"{h:02d}:{m:02d}:{s:06.3f}"

try:
	(opts, args) = getopt.getopt(sys.argv[1:], '', [
		'video_name=',
		'load_weights='
	])
	if len(opts) != 2:
		raise ''
except:
	print('usage: python3 predict3.py --video_name=<videoPath> --load_weights=<weightPath>')
	exit(1)

for (opt, arg) in opts:
	if opt == '--video_name':
		videoName = arg
	elif opt == '--load_weights':
		load_weights = arg
	else:
		print('usage: python3 predict3.py --video_name=<videoPath> --load_weights=<weightPath>')
		exit(1)

# 损失
def custom_loss(y_true, y_pred):
	loss = (-1)*(K.square(1 - y_pred) * y_true * K.log(K.clip(y_pred, K.epsilon(), 1)) + K.square(y_pred) * (1 - y_true) * K.log(K.clip(1 - y_pred, K.epsilon(), 1)))
	return K.mean(loss)

model = load_model(load_weights, custom_objects={'custom_loss':custom_loss,  'Adadelta': tf.keras.optimizers.Adadelta(learning_rate=1.0)})
model.summary()
print('Beginning predicting......')

start_after_model_load = time.time()

# 当前目录,以及需要output的文件夹路径
# current_path = os.getcwd()
# output_folder = os.path.join(current_path, 'output')
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# f = open(videoName[:-4]+'_predict.csv', 'w')
# f = open(videoName[:-4] + '.csv', 'w')
# f.write('Frame,Visibility,X,Y,Time\n')
csv_writer = csv.writer(open(videoName[:-4] + '.csv', 'w', newline=''))
csv_writer.writerow(['Frame','Visibility','X','Y','Time'])

cap = cv2.VideoCapture(videoName)

success, image1 = cap.read()
frame_time1 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
success, image2 = cap.read()
frame_time2 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
success, image3 = cap.read()
frame_time3 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
# success, image4 = cap.read()
# frame_time4 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
# success, image5 = cap.read()
# frame_time5 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
# success, image6 = cap.read()
# frame_time6 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))

ratio = image1.shape[0] / HEIGHT

size = (int(WIDTH*ratio), int(HEIGHT*ratio))
fps = cap.get(5)
print(fps)

if videoName[-3:] == 'avi':
	fourcc = cv2.VideoWriter_fourcc(*'DIVX')
elif videoName[-3:] == 'mp4':
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
else:
	print('usage: video type can only be .avi or .mp4')
	exit(1)

# out = cv2.VideoWriter(videoName[:-4]+'_predict'+videoName[-4:], fourcc, fps, size)

count = 0
no_game_flag = 0
pre_x = 0
pre_y = 0

while success:
    start_time = time.time()
    if no_game_flag > 6000:
        break
    # 调整 BGR format (cv2) to RGB format (PIL)
    x1 = image1[...,::-1]
    x2 = image2[...,::-1]
    x3 = image3[...,::-1]
    # 调整 np arrays to PIL images
    x1 = array_to_img(x1)
    x2 = array_to_img(x2)
    x3 = array_to_img(x3)
    # resize
    x1 = x1.resize(size = (WIDTH, HEIGHT))
    x2 = x2.resize(size = (WIDTH, HEIGHT))
    x3 = x3.resize(size = (WIDTH, HEIGHT))
    # Convert images to np arrays and adjust to channels first
    x1 = np.moveaxis(img_to_array(x1), -1, 0)
    x2 = np.moveaxis(img_to_array(x2), -1, 0)
    x3 = np.moveaxis(img_to_array(x3), -1, 0)
    # 生成data
    unit = np.concatenate([x1, x2, x3], axis=0)
    unit = unit.reshape((1, 9, HEIGHT, WIDTH))
    unit = unit.astype('float32')
    unit /= 255
    y_pred = model.predict(unit, batch_size=BATCH_SIZE)
    y_pred = y_pred > 0.5
    y_pred = y_pred.astype('float32')
    h_pred = y_pred[0]*255
    h_pred = h_pred.astype('uint8')
    for i in range(3):
        if i == 0:
            frame_time = frame_time1
            # frame_time_next = frame_time2
            image = image1
        elif i == 1:
            frame_time = frame_time2
            # frame_time_next = frame_time4
            image = image2
        elif i == 2:
            frame_time = frame_time3
            # frame_time_next = frame_time6
            image = image3
        if np.amax(h_pred[i]) <= 0:
            # f.write(str(count)+',0,0,0,'+frame_time+'\n')
            csv_writer.writerow([count, '0', '0', '0', frame_time])
            # csv_writer.writerow([count+1, '0', '0', '0', frame_time_next])
            no_game_flag += 1
            # out.write(image)
        else:    
            #h_pred
            (cnts, _) = cv2.findContours(h_pred[i].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            rects = [cv2.boundingRect(ctr) for ctr in cnts]
            max_area_idx = np.argmax([r[2]*r[3] for r in rects])
            target = rects[max_area_idx]
            (cx_pred, cy_pred) = (int(ratio*(target[0] + target[2] / 2)), int(ratio*(target[1] + target[3] / 2)))
            # f.write(str(count)+',1,'+str(cx_pred)+','+str(cy_pred)+','+frame_time+'\n')
            csv_writer.writerow([count, '1', cx_pred, cy_pred, frame_time])
            # 可能导致球速测算的问题，暂时先这样，需要再改！！
            # csv_writer.writerow([count+1, '1', int((cx_pred + pre_x)/2) , int((cy_pred + pre_y)/2) , frame_time_next])
            pre_x = cx_pred
            pre_y = cy_pred
            image_cp = np.copy(image)
            # cv2.circle(image_cp, (cx_pred, cy_pred), 5, (0,0,255), -1)
            # out.write(image_cp)
        count += 1
        # print('count is ', count )
    success, image1 = cap.read()
    frame_time1 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
    success, image2 = cap.read()
    frame_time2 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
    success, image3 = cap.read()
    frame_time3 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
    # success, image4 = cap.read()
    # frame_time4 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
    # success, image5 = cap.read()
    # frame_time5 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
    # success, image6 = cap.read()
    # frame_time6 = custom_time(cap.get(cv2.CAP_PROP_POS_MSEC))
    end_time = time.time()
    # print(f"Processed frame {count} in {end_time - start_time:.3f} seconds")


cap.release()


# f.close()
# out.release()
# csv_writer.close()
end = time.time()
print('Prediction time:', end-start, 'secs')
print('After time:', end-start_after_model_load, 'secs')
# with open('all_data.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerows('this is algorithm time '+str(end-start))
# import openpyxl
# workbook = openpyxl.load_workbook('all_data.xlsx')
# workbook = workbook.active
# workbook.append(['this is algorithm time ',str(end-start)])
# workbook.save('all_data.xlsx')
# print('Done......')




# import pandas as pd

# # 读取现有 xlsx 文件
# df = pd.read_excel('all_data.xlsx', sheet_name='Sheet1', engine='openpyxl', index_col=0)
# # 创建写入的数据
# new_data = pd.Series(['this is algorithm time '+ str(end- start)])

# # 添加新的行
# df['row'] = df['row'].append(new_data)

# # 写出到 xlsx 文件
# df.to_excel('all_data.xlsx', sheet_name='Sheet1')  
now = datetime.datetime.now(tz)  
end_datatime_str = now.strftime('%Y-%m-%d %H:%M:%S')  
with open('/home/sportvision/highlight_code/alg_time.txt', 'a') as f:
    new_string = datatime_str + ',' + str(end- start) + ',' +  end_datatime_str + ',' + str(end-start_after_model_load) + '\n'
    f.write(new_string + '\n')
