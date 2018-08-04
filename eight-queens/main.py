import cv2
import numpy as np
import os
import subprocess
import identify_demo as id

#初始化摄像头、串口
cap = cv2.VideoCapture(0)
cap.set(3,300)
cap.set(4,300)

ser = serial.Serial("dev/ttyS0", 115200, timeout = 3)

#输入路径
route = [41, 55, 39, 22]

#初始化起点
origin = cv2.
current_pos = id.identify_num
