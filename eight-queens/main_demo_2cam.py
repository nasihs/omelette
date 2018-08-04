import sys
import cv2
import time
import serial
import identify_demo as id


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

#fps = cap1.get(5)  #获取FPS

ser = serial.Serial("dev/ttyAMA0", 115200, timeout = 3)

id.cam_init()

while (True):
    try:
        success0 = cap0.grab()
        success1 = cap1.grab()
    except:
        print ("grab failed")
        sys.exit()
    else:
        frame0 = cap0.retrieve()
        frame1 = cap1.retrieve()
    
    #ret, frame = cap0.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("camera00", frame0)
    cv2.imshow("camera01", frame1)
    diff1, diff2 = (id.identify_mid(frame1))
    diff3, diff4 = (id.identify_mid(frame2))
    print (diff1, diff2)
    print (diff3, diff4)
    #list = [OxA5 diff1 diff2]
    ser.write(OxA5)
    ser.write(diff1)
    ser.write(diff2)
    ser.write(0xB3)
    ser.write(diff3)
    ser.write(diff4)

    
    if cv2.waitKey(1) & 0xFF == ord("q"):
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

    


