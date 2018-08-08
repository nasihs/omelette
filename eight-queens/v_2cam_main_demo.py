#/usr/bin/python3

import sys
import cv2
#import time
import serial
import identify_demo as id


print ("camera initializing...")
cap0 = cv2.VideoCapture(1)
cap1 = cv2.VideoCapture(0)
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

#fps = cap1.get(5)  #获取FPS

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout = 3)

#id.cam_init()

while (True):
    try:
        """
        cap0.grab()
        cap1.grab()
        frame0 = cap0.retrieve()
        frame1 = cap1.retrieve()
        """
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()
    except:
        print ("cap.read failed")
        cap0.release()
        cap1.release()
        sys.exit()
    
    #ret, frame = cap0.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    try:
        cv2.imshow("camera00", frame0)
        cv2.imshow("camera01", frame1)
    except:
        print ("capture failed")
        cap0.release()
        cap1.release()
        print ("program exiting...")
        sys.exit()
    try:
        diff1, diff2 = (id.identify_mid(frame0))
        diff3, diff4 = (id.identify_mid(frame1))
    except:
        print("identify_mid failed")
        cap0.release()
        cap1.release()
        sys.exit()
        
    if diff1 > 255:
        diff1 = 255 
    d1 = int(diff1)
    d2 = int(diff2)
    print (d1, d2)
    if diff3 > 255:
        diff3 = 255
    d3 = int(diff3)
    d4 = int(diff4)
    print (d3, d4)
    #list = [OxA5 diff1 diff2]
    ser.write([0xA5])
    ser.write([d1])
    ser.write([d2])
    ser.write([d3])
    ser.write([d4])

    
    if cv2.waitKey(5) & 0xFF == ord("q"):
        cap0.release()
        cap1.release()
        cv2.destroyAllWindows()
        break
    

''' 
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
 '''

    


