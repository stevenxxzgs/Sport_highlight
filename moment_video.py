import csv
import sys
import time
import os
import pandas as pd

start_time = time.time()

# 文件路径
current_path = os.getcwd()
output_folder = os.path.join(current_path, 'output/moment_csv')
output_folder_test = os.path.join(current_path, 'output/moment_csv_test')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# print(output_folder)

# 输入参数需要有一个文件名
if len(sys.argv) < 2:
    print("Usage: python script.py input_file.csv")
    exit()

input_file_name = sys.argv[1]
csv_path = os.path.join(current_path, 'output/sub_video/')
input_filepath = os.path.join(csv_path, input_file_name)

# with open(input_filepath) as f:
#     reader = csv.reader(f)
#     input_data = list(reader)

# 保留文件名
name, _ = input_file_name.split('.')
name =  name + '.csv'
# print(name)
filepath = os.path.join(output_folder, name)
filepath_test = os.path.join(output_folder_test, name)


df = pd.read_csv(input_filepath)
# 创建辅助列 roll_vis,计算前后三个 Visibility 值
# df['roll_vis'] = df['Visibility'].rolling(3).sum()
df['roll_vis'] = df['Visibility'].rolling(5, center=True).sum()

for i in range(len(df)):
    if df.loc[i, 'Y'] < 15 and df.loc[i,'Y'] > 0 and df.loc[i, 'X'] > 0:
        # print('this line is ', df.loc[i, 'Y'], df.loc[i, 'roll_vis'])
        df.loc[i, 'roll_vis'] = 8.0

# # 定义条件
# condition = (df['roll_vis'] >= 2)

# # 根据条件修改 Visibility 值
# df.loc[condition, 'Visibility'] = 1
# df.loc[~condition, 'Visibility'] = 0

# condition = (df['roll_vis'] == 1 and df['X'] != 0 and df['Y'] != 0)
# condition = ((df['roll_vis'] >= 1) & (df['X'] != 0) & (df['Y'] != 0))
# df.loc[condition, 'Visibility'] = 1
# df.loc[~condition, 'Visibility'] = 0

# j = len(df) - 2
# for i in range(2, j):
#     if df.loc[i, 'Visibility'] == 1:
#         if df.loc[i-1, 'Visibility'] == 0 and df.loc[i+1, 'Visibility'] == 0 and df.loc[i-2, 'Visibility'] == 0 and df.loc[i+2, 'Visibility'] == 0 :
#             df.loc[i, 'Visibility'] = 0
#             df.loc[i, 'X'] = 0
#             df.loc[i, 'Y'] = 0
#             # df.loc[i, 'X'] = ( df.loc[i-1, 'X'] + df.loc[i+1, 'X'] )/ 2
#             # df.loc[i, 'Y'] = ( df.loc[i-1, 'Y'] + df.loc[i+1, 'Y'] )/ 2
#     else:
#         continue
# remove_df = df
# remove_df = remove_df.drop('roll_vis', axis=1)
# remove_df.to_csv(filepath_test + "_removezero.csv", index = False)


j = len(df) - 2
for i in range(1, j):
    if df.loc[i, 'Visibility'] == 1 and df.loc[i+1, 'Visibility'] == 1 and df.loc[i+2, 'Visibility'] == 1:
        if abs(df.loc[i, 'X']-df.loc[i+1, 'X']) + abs(df.loc[i, 'Y']-df.loc[i+1, 'Y']) < 3 :
            df.loc[i, 'Visibility'] = 0
            df.loc[i+1, 'Visibility'] = 0
            df.loc[i+2, 'Visibility'] = 0
    else:
        continue

j = len(df) - 2
for i in range(1, j):
    if df.loc[i, 'Visibility'] == 1 and df.loc[i+1, 'Visibility'] == 1 :
            if abs(df.loc[i, 'X']-df.loc[i+1, 'X']) + abs(df.loc[i, 'Y']-df.loc[i+1, 'Y']) < 3 :
                df.loc[i, 'Visibility'] = 0
                df.loc[i+1, 'Visibility'] = 0
    else:
        continue            
# df.to_csv(filepath_test + "_newtest.csv")




df_rev = df.loc[::-1]

j = len(df_rev) - 1
for i in range(1,len(df_rev)-1):
    if df_rev.loc[j-i, 'roll_vis'] == 8.0:
        while(j-i-1 >=0 and df_rev.loc[j-i-1,'Visibility'] == 0 and df_rev.loc[j-i-1, 'Y']==0 ):
            df_rev.loc[j-i-1, 'Visibility'] = 1
            i+=1


df = df_rev.loc[::-1]

df['count_00'] = 0  
df['count_11'] = 0

zero_count = 0 
one_count = 0

count_0 = 0
count_1 = 0
for i in range(len(df)):
    x = df.loc[i, 'X']
    y = df.loc[i, 'Y']
    
    if (x == 0) and (y == 0):
        zero_count += 1
        if zero_count == 2:
            count_0 += 1  
            one_count = 0     
        df.loc[i, 'count_00'] = count_0  
    elif (x != 0) and (y != 0): 
        one_count += 1   
        if one_count == 2:
            count_1 += 1     
            zero_count = 0
        df.loc[i,'count_11'] = count_1       

df.to_csv(filepath_test + "_testcsvout.csv")

df['count_total'] = df['count_00'] + df['count_11']
# 删除辅助列
df.drop('roll_vis', axis=1, inplace=True)
df.drop('count_00', axis=1, inplace=True)
df.drop('count_11', axis=1, inplace=True)
input_data = df.values.tolist()
# print(df)
# print(input_data)



output_forward = []
start = None
end = None
start_y_station = None
end_y_station = None
start_bout = None
end_bout = None
count = 0 
end_count = 0
thredhold = 30
# 进行精彩回合的收集
for row in input_data:
    y = row[3]
    # print(row)
    if row[1] == 1:
        if start == None:
            start = row[4]
            start_y_station = row[3]
            start_bout = row[5]
        # end = row[4] 
        # count += 1
        if start != None and count != 0:
            count = 0
        if y == 0:
            continue
        elif y < 40 and y > 0: # 30
            thredhold = 200
        else:
            thredhold = 30
    else:
        if count >= thredhold: # 中间可以空多少个未检测
            end = row[4]
            end_y_station = row[3]
            end_bout = row[5]
            end_count = count
            output_forward.append([start, end, end_count, end_bout-start_bout, start_y_station, end_y_station])
            start = None
            end = None
            count = 0
        if start != None:
            count += 1

if start != None:
    end = row[4]
    end_y_station = row[3]
    end_bout = row[5]
    end_count = count
    # print('count  end ', end_count)
    output_forward.append([start, end, end_count, end_bout-start_bout, start_y_station, end_y_station])



results = []
changeCamTime = 2
start_cam = 2
res =[]
# 时间解析与排序, bout:回合数目
for t1, t2, end_count, bout, start_y_station, end_y_station in output_forward:
    if start_y_station <= 120:
        start_cam = 3
        end_cam = 2
    else:
        start_cam = 2
        end_cam = 3
    
    h1, m1, s1 = t1.split(':')
    h2, m2, s2 = t2.split(':')
    h1 = int(h1)
    m1 = int(m1)
    h2 = int(h2)
    m2 = int(m2)
    s1 = float(s1[:len(s1) - len(s1.split('.')[1]) + 7])
    s2 = float(s2[:len(s2) - len(s2.split('.')[1]) + 7])
    if s1 > 0.5:
        s1 = s1-1
    s2 = s2 - end_count*0.04 + 1
    # else:
    #     s2 = s2 - 2.5
    
    time1 = h1*3600 + m1*60 + s1
    time2 = h2*3600 + m2*60 + s2
    diff = time2 - time1
    
    t_change_cam = time1 - changeCamTime
    if t_change_cam >=0 :
        change_hours = int(t_change_cam // 3600)
        change_minutes = int((t_change_cam % 3600) // 60) 
        change_seconds = int(t_change_cam % 60)
    else:
        change_hours = 0
        change_minutes = 0
        change_seconds = 0  
    hc = format(change_hours, '02')
    mc = format(change_minutes, '02')
    sc = format(change_seconds, '02.2f')
    t_change_start = f'{hc}:{mc}:{sc}'


    t_change_cam = time2 - changeCamTime - 5
    change_hours = int(t_change_cam // 3600)
    change_minutes = int((t_change_cam % 3600) // 60) 
    change_seconds = int(t_change_cam % 60)
    hc = format(change_hours, '02')
    mc = format(change_minutes, '02')
    sc = format(change_seconds, '02.2f')
    t_change_end = f'{hc}:{mc}:{sc}'


    print('t_change_start ', t_change_start)
    print('t_change_start ', t_change_end)
    h1 = format(h1, '02')
    m1 = format(m1, '02')
    s1 = format(s1, '02.2f')
    t1_new = f'{h1}:{m1}:{s1}'

    h2 = format(h2, '02')
    m2 = format(m2, '02')
    s2 = format(s2, '02.2f')
    t2_new = f'{h2}:{m2}:{s2}'
    # print('t1 is' ,t1, ';/; t2 is', t2)  
    # if diff > 3:
    # print('round time is ', diff)
        # results.append([diff, t1_new, t2_new, changeCamTime, t_change_start, start_cam, t_change_end, end_cam])
    if diff > 0 and  ( bout > diff or ( diff > 5 and diff-bout < 1 ) ) :
        res.append([diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam])

# print(type(res))
# file_path = "data.csv"

# with open(file_path, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(res)
# 找到可以合并的集锦
result = []
# res.sort(reverse=True)
for i in range(len(res)-1):
    diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam = res[i]
    diff_next, t1_new_next, t2_new_next, bout_next, time1_next, time2_next, changeCamTime_next, t_change_start_next, start_cam_next, t_change_end_next, end_cam_next = res[i+1]
    if( time1_next < time2 ):
        result.append([diff+diff_next, t1_new, t2_new_next, bout+bout_next, time1, time2_next, changeCamTime, t_change_start, start_cam, t_change_end_next, end_cam_next])
    else:
        result.append([diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam])

diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam = res[-1]
result.append([diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam])

# 合并间隔只有0.5的集锦
# results = []
# for i in range(len(result)-1):
#     diff, t1_new, t2_new, bout, time1, time2 = result[i]
#     diff_next, t1_new_next, t2_new_next, bout_next, time1_next, time2_next = result[i+1]
#     if( time1_next - time2 < 0.5):
#         results.append([diff+diff_next, t1_new, t2_new_next, bout+bout_next])
#     else:
#         results.append([diff, t1_new, t2_new, bout])


# 合并间隔0.5的集锦
results = []
temp = []
for diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam in result:
    if not temp:
        temp.append([diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam])
    else:
        diff_last, t1_new_last, t2_new_last, bout_last, time1_last, time2_last, changeCamTime_last, t_change_start_last, start_cam_last, t_change_end_last, end_cam_last = temp[-1]
        if time1 - time2_last < 0.1:
            temp = []
            temp.append([diff + diff_last, t1_new_last, t2_new, bout, time1_last, time2, changeCamTime_last, t_change_start_last, start_cam_last, t_change_end, end_cam])
        else:
            results.extend(temp)
            temp = []
            temp.append([diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam])
if temp:
    results.extend(temp)

final_result = []
for diff, t1_new, t2_new, bout, time1, time2, changeCamTime, t_change_start, start_cam, t_change_end, end_cam in results:
    if diff > 5 and bout - diff < 15:
        final_result.append([diff, t1_new, t2_new, changeCamTime, t_change_start, start_cam, t_change_end, end_cam, bout/diff])

final_result.sort(key= lambda x: x[8],reverse=True)
top_5 = final_result[:5]


# 文件保留
if len(final_result) != 0:
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(top_5)

with open(filepath_test, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(final_result)



end_time = time.time()

print("time is ", end_time- start_time)
# with open('all_data.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerows('this is momentvideo time '+str(end_time- start_time) )



# import openpyxl
# workbook = openpyxl.load_workbook('all_data.xlsx')
# workbook = workbook.active
# workbook.append(['this is momentvideo time ',str(end_time- start_time)])
# workbook.save('all_data.xlsx')


# import pandas as pd

# # 读取现有 xlsx 文件
# df = pd.read_excel('all_data.xlsx', sheet_name='Sheet1', engine='openpyxl', index_col=0)

# # 创建写入的数据
# new_data = pd.Series(['this is momentvideo time '+str(end_time- start_time)])

# # 添加新的行
# df['row'] = df['row'].append(new_data)

# # 写出到 xlsx 文件
# df.to_excel('all_data.xlsx', sheet_name='Sheet1')  


with open('time.txt', 'a') as f:
    new_string = str(len(results) )+ ','
    f.write(new_string )