import cv2
import time

def capture_pic():
    cap = cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)

    i = 1

    while (1):
        start = time.clock()
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            #fileName = "Capture_0{}.png".format(i)
            #cv2.imwrite("fileName", frame)
            cv2.imwrite("capture0%d.png" % i, frame)
            i = i + 1
        elif cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break
        elapsed = 1/(time.clock() - start)
        print("FPS:", elapsed)




capture_pic()

