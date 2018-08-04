import cv2
import time
import serial
import identify_demo as id

cap = cv2.VideoCapture(0)
cap.set(3,300)
cap.set(4,300)

#ser = serial.Serial("dev/ttyS0", 115200, timeout = 3)

ser=serial.Serial("COM3",256000)
while (True):
    ret, frame = cap.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("camera01", frame)
    diff1, diff2 = (id.identify_mid(frame))
    print (diff1, diff2)
    #list = [OxA5 diff1 diff2]
    ser.write (OxA5)
    ser.write(OxA5)
    ser.write(OxA5)

    """
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cap.release()
        cv2.destroyAllWindows()
        break
    """


    


