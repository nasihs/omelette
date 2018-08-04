#-*- coding:utf-8 -*-

import cv2
import math
import numpy as np
import os
import sys
import subprocess
import pytesseract

def identify_num(img):
    """
    识别图像中的数字
    
    Args:
        img：摄像头获取的图像
        tresh：二值化后的图像
        kernel:膨胀算法卷积核
        dilation：膨胀处理后的图像
    Returns:
        result：识别结果
    """


    if img.shape[0] > 300:
        img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    (_, tresh) = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    kernel = np.ones((6, 6),np.uint8)
    dilation = cv2.dilate(tresh, kernel, iterations = 1)
    #cv2.imwrite('rec.png', dilation)
    
    try:
        result = pytesseract.image_to_string(dilation, config = '-psm 7 digits')
    except:
        result = 777    #识别失败
        #print("Identify Failed")
    return result


def identify_angle(img):
    """
    识别摄像头捕捉图像中横线倾斜角度
    """


    if img.shape[0] > 240:
        img = cv2.resize(img, (320, 240), interpolation=cv2.INTER_AREA)
    #Sobel算子计算y方向梯度
    y = cv2.Sobel(img,cv2.CV_16S,0,1)
    absY = cv2.convertScaleAbs(y)
    (_, thresh) = cv2.threshold(absY, 200, 255, cv2.THRESH_BINARY)

    """
    #HoughlinesP检测横线
    # minLineLength = 500
    # maxLineGap = 40
    lines = cv2.HoughLinesP(thresh, 1, np.pi / 180, 100, minLineLength=0.9 * img.shape[1],
                            maxLineGap=0.1 * img.shape[0])
    nline = len(lines)
    angle_array = np.zeros([nline, 1])
    for i in range(nline):
        x1, y1, x2, y2 = lines[i][0]
        #cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)   #在图像中绘制直线
        x_coord = lines[i][0][2] - lines[i][0][0]
        y_coord = lines[i][0][3] - lines[i][0][1]
        angle = math.atan2(y_coord, x_coord) * 180 / math.pi
        angle_array[i] = angle
    angle = np.mean(angle_array)
    """

    #Houghlines检测直线
    try:
        lines = cv2.HoughLines(thresh, 1, np.pi/180, 200)
        angle = 90 - lines[0][0][1] / np.pi * 180
    except TypeError:
        angle = 666
    #angle = 90 - lines[0][0][1]/np.pi * 180
    return angle
    # print(angle_array)


def identify_mid(img):
    """
    识别中线偏差
    """
    

    if img.shape[0] > 240:
        img = cv2.resize(img, (320, 240), interpolation=cv2.INTER_AREA)

    #(img,G,R) = cv2.split(img)#提取R、G、B分量

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    (_, thresh) = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV)
    (thresh, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)
    #print (c)
    #tmp = np.zeros(thresh.shape, np.uint8)
    #cv2.drawContours(tmp, c, 0, 255, 1)

    cnt = c[0]

    #轮廓近似
    epsilon = 0.1*cv2.arcLength(cnt,True)
    cnt = cv2.approxPolyDP(cnt,epsilon,True)

    rect = cv2.minAreaRect(cnt) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    #box = cv2.boxPoints(rect) #for OpenCV 3.x 获取最小外接矩形的4个顶点
    #box = np.int0(box)


    # 调整摄像头位置角度 务必使找到的矩形中心和摄像头视野中心重合
    x_error = 160 - rect[0][0]  #横向偏差
    y_error = 120 - rect[0][1]  #纵向偏差

    #print (box)
    #cv2.drawContours(img, [box], 0, (0,0, 255), 2)
    """"
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    error = ([x_error, y_error])
    return error
    

def cam_init():
    print ("camera initializing")
    cap0 = cv2.VideoCapture(0)
    cap1 = cv2.VideoCapture(1)
    cap0.set(3, 320)
    cap0.set(4, 240)
    cap1.set(3, 320)
    cap1.set(4, 240)

    if cap0.isOpened and cap1.isOpened:
        print ("cameras are opened")
    else:
        print ("cameras are not opened")
        print ("program exiting...")
        sys.exit()
    
    print ("FPS0:", cap0.get(5))
    print ("FPS1:", cap1.get(5))
    print ("camera successfully initialized")

    


if __name__ == "__main__":
    import time


    img = cv2.imread("./pics/origin/capture01.png")
    start = time.clock()
    print ("识别结果",identify_num(img))


    elapsed = (time.clock() - start)
    print("Time used:",elapsed)

