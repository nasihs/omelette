# -*- coding:utf-8 -*-

"""
自动前进
加入了多线程通信
加入了自动计算步数

"""

import cv2
import numpy as np
import sys
import subprocess
import identify_demo as id
from multiprocessing import Process, Queue


def count_blocks():
    pass


def move_forward(temp, fwd, q):
    flag = 1
    while True:
        coor = q.get(True)
        if temp == 0:
            # 停车
            ser.write([0x5A]) # 头帧
            ser.write([0x01]) # 方向
            ser.write([0x00]) # 速度
            break
        
        # 平移
        if fwd:
            # 前进
            ser.write([0x5A]) # 头帧
            ser.write([0x0]) 
            pass
        else:
            # 后退
            # ser.write()
            # ser.write()
            pass

        # 判断是否下一格
        if flag == 1 and (coor[1] == center[1]):
            flag =  0
            temp -= 1
        #print (temp)
        
        if coor[1] != center[1]:
            flag = 1
        else:
            flag = 0



def move_right(temp, rht, q):
    flag = 1
    while True:
        coor = q.get(True)
        if temp == 0:
            # 停车
            # ser.write()
            # ser.write()
            break
        
        # 平移
        if rht:
            # 右移
            # ser.write()
            # ser.write()
            pass
        else:
            # 左移
            # ser.write()
            # ser.write()
            pass

        # 判断是否下一格
        if flag == 1 and (coor[1] == center[1]):
            flag =  0
            temp -= 1
        #print (temp)
        
        if coor[1] != center[1]:
            flag = 1
        else:
            flag = 0
        

def recognize(q):
    print ("camera initializing...")
    cap0 = cv2.VideoCapture(0)
    cap0.set(3,320)
    cap0.set(4,240)

    
    if cap0.isOpened:
        print ("cameras are opened")
    else:
        print ("cameras are not opened")
        print ("program exiting...")
        sys.exit()
    print ("FPS0:", cap0.get(5))
    print ("cameras successfully initialized")

    while True:
        try:
            ret0, frame0 = cap0.read()
        except:
            print ("cap0.read failed")
            cap0.release()
            sys.exit()
        
        #ret, frame = cap0.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        try:
            cv2.imshow("camera0", frame0)
        except:
            print ("capture failed")
            cap0.release()
            print ("exiting...")
            sys.exit()
        try:
            diff1, diff2 = (id.identify_mid(frame0))
        except:
            print("identify_mid failed")
            cap0.release()
            sys.exit()
            
        if diff1 > 255:
            diff1 = 255 
        d1 = int(diff1)
        d2 = int(diff2)
        #coor = (d1, d2)
        #print (coor)
        q.put((d1, d2))
        

        
        if cv2.waitKey(5) & 0xFF == ord("q"):
            cap0.release()
            cv2.destroyAllWindows()
            break
        
        ret, frame = cap0.read()
        print (ret)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("camera01", frame)
        diff1, diff2 = id.identify_mid(frame)
        #print(diff1)
        if diff1 > 255:
            diff1 = 255
        d1 = int(diff1)
        d2 = int(diff2)
        print (d1,d2)
        #list = []
        ser.write([0xA5])
        ser.write([d1])
        ser.write([d2])
        
        #time.sleep(0.2)
        q.put((d1, d2))

        if cv2.waitKey(1)   == ord("q"):
            cap0.release()
            cv2.destroyAllWindows()
            break


def auto_move(q):
    for i in steps:
        # coor = q.get(True)
        forward = i[0] < 0
        temp_x = abs(i[0])
        right = i[1] > 0
        temp_y = abs(i[1])
        move_forward(temp_x, forward, q)
        move_right(temp_y, right, q)

        
        ''' 
        print (i)
        while True:
            # dx, dy为正：向左或下平移
            if i[0] != 0:
                temp = abs(i[0])
                for k in range(temp):
                # 向左移动
                # ser.write (OxA5)
        '''



if __name__ == "__main__":
    # 设定摄像头中心坐标
    center = (160, 120)

    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout = 3)
    """
    #初始化摄像头、串口
    cap1 = cv2.VideoCapture(0)
    cap1.set(3,300)
    cap1.set(4,300)

    #ser = serial.Serial("dev/ttyS0", 115200, timeout = 3)

    ''' 
    #识别起点 
    ret, frame = cap1.read()
    origin = [id.identify_num(frame)]
    '''

    """

    # origin为入场位置
    origin = [57]
    #输入路径
    #route = [41, 55, 39, 22]
    route1 = [42, 26, 32, 8]
    # 总路径
    route = origin + route1
    print ("总路径为:", route)

    # 棋盘坐标系
    map = {"1": (1, 1), "2": (2, 1), "3": (3, 1), "4": (4, 1),
            "5": (5, 1), "6": (6, 1), "7": (7, 1), "8": (8, 1),
            "9": (1, 2), "10": (2, 2), "11": (3, 2), "12": (4, 2),
            "13": (5, 2), "14": (6 ,2), "15": (7, 2), "16": (8, 2),
            "17": (1, 3), "18": (2, 3), "19": (3, 3), "20": (4, 3),
            "21": (5, 3), "22": (6, 3), "23": (7, 3), "24": (8, 3),
            "25": (1, 4), "26": (2, 4), "27": (3, 4), "28": (4, 4),
            "29": (5, 4), "30": (6, 4), "31": (7, 4), "32": (8, 4),
            "33": (1, 5), "34": (2, 5), "35": (3, 5), "36": (4, 5),
            "37": (5, 5), "38": (6, 5), "39": (7, 5), "40": (8, 5),
            "41": (1, 6), "42": (2, 6), "43": (3, 6), "44": (4, 6),
            "45": (5, 6), "46": (6, 6), "47": (7, 6), "48": (8, 6),
            "49": (1, 7), "50": (2, 7), "51": (3, 7), "52": (4, 7),
            "53": (5, 7), "54": (6, 7), "55": (7, 7), "56": (8, 7),
            "57": (1, 8), "58": (2, 8), "59": (3, 8), "60": (4, 8),
            "61": (5, 8), "62": (6, 8), "63": (7, 8), "64": (8, 8)}

    # 从route中一个坐标移动到下一个坐标为一个step
    steps = []
    for i in range(1, len(route)):
        x2 = map[str(route[i])][0]
        x1 = map[str(route[i - 1])][0]
        dx = x2 - x1
        y2 = map[str(route[i])][1] 
        y1 = map[str(route[i - 1])][1]
        dy = y2 - y1
        steps.append((dx, dy))

    # dx, dy为每次移动时x, y轴移动的格数
    print ("步骤:", steps)

    q = Queue()
    p_rec = Process(target = recognize, args = (q,))
    p_mov = Process(target = auto_move, args = (q, steps))
    p_rec.start()
    p_mov.start()
    p_mov.join()
    p_rec.terminate()
    print ("done")
    sys.exit()


