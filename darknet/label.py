import os
import glob
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

result_file_list = sorted(glob.glob("results/*.txt"))
res = []
thresh = 0.6
for resfile in result_file_list:
    df = pd.read_csv(resfile, sep=' ', header=None)
    res.append(df[df[1]>thresh])

label = ['Kangshifu Xiangla', 'Tongyi Laotan', 'Tongyi Xiangla']
classes = 3
colors = [(255,0,0), (0,255,0), (0,0,255)]
savedir = 'results/image'

image_file_list = sorted(glob.glob("data/test_images/*.jpeg"))
for file in image_file_list:
    # 读取图片
    image = cv2.imread(file)
    name = file.split('/')[-1].split('.')[0]
    # 逐类别处理
    for class_i in range(classes):
        # 读取本类别颜色
        color = colors[class_i]
        # 读取本类别识别结果
        df = res[class_i]
        # 读取本类别本图片识别结果
        boxes = df[df[0]==name].values
        # 对每个结果绘制框
        for box in boxes:
            # 读取框坐标
            x, y, w, h = box[2:].astype(np.int32)
            # 绘制框
            cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)
            # 绘制文本
            cv2.putText(image, label[class_i], (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    cv2.imwrite(os.path.join(savedir, name+'.jpeg') ,image)
