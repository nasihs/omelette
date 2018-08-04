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


    def __image_to_string(img, cleanup=True, plus=''):
        """
        shell方式调用tesseract
           
        """


        # cleanup为True则识别完成后删除生成的文本文件
        # plus参数为给tesseract的附加高级参数
        subprocess.check_output('tesseract ' + img + ' ' +
                            img + ' ' + plus, shell=True)  # 生成同名txt文件
        text = ''
        with open(img + '.txt', 'r') as f:
            text = f.read().strip()
        if cleanup:
            os.remove(img + '.txt')
        return text
        #print(image_to_string('./pics/cap24_dil.png', True, '-psm 7 digits'))


    if img.shape[0] > 300:
        img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    (_, tresh) = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    kernel = np.ones((6, 6),np.uint8)
    dilation = cv2.dilate(tresh, kernel, iterations = 1)
    #cv2.imwrite('rec.png', dilation)
    
    try:
        result = __image_to_string('rec.png', True, '-psm 7')
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
    cv2.imwrite("39_origin.png", img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("./pics/39_gray2.png", gray)
    (_, thresh) = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("./pics/39_thresh.png", thresh)
    (thresh, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)

    tmp = np.zeros(thresh.shape, np.uint8)
    cv2.drawContours(tmp, c, 0, 255, 2)
    cv2.imwrite("./jishubaogao/39_tmp2.png", tmp)
    #角点检测
    kp = cv2.goodFeaturesToTrack(tmp, 4, 0.04, 10)
    kp = np.int0(kp)

    pix = []
    for i in kp:
        x,y = i.ravel()
        img[y, x] = [0, 0, 255]
        pix.append([x,y])
    pix = sorted(pix, key=lambda x:x[1], reverse=True)
    print(pix)
    cv2.drawContours(img, c, 0, (0, 0, 255), 2)
    cv2.imwrite("./jishubaogao/39_kuang.png", img)


    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    x_error = int(img.shape[0] - pix[0][1])
    y_error = int((pix[0][0] + pix[1][0])/2 - img.shape[1]/2)
   

    return x_error, y_error 
    
    
        



if __name__ == "__main__":
    import time

    img = cv2.imread("./pics/39_cap.jpg")
    start = time.clock()
    print(identify_mid(img))


    elapsed = (time.clock() - start)
    print("Time used:",elapsed)

