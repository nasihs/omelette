#coding=utf-8
import cv2
import numpy as np

import time
start = time.clock()
 
img = cv2.imread("./pics/47_cap.jpg", 0)
#img = cv2.resize(img, (320, 240), interpolation=cv2.INTER_AREA)
print (img.shape[0])
img2 =cv2.imread("./pics/47_cap.jpg", cv2.IMREAD_COLOR)
#img2 = cv2.resize(img2, (320, 240), interpolation=cv2.INTER_AREA)
#x = cv2.Sobel(img,cv2.CV_16S,1,0)
y = cv2.Sobel(img,cv2.CV_16S,0,1)
 
#absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)

(_, thresh) = cv2.threshold(absY, 200, 255, cv2.THRESH_BINARY)

lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 100, minLineLength=500, maxLineGap=40)
print(lines)
for i in range(len(lines)):
    x1, y1, x2, y2 = lines[i][0]
    cv2.line(img2, (x1, y1), (x2, y2), (0, 0, 255), 3)
cv2.imshow("img", img2)
img2 = cv2.resize(img2, (160, 120), interpolation=cv2.INTER_AREA)
cv2.imwrite("./angle_lines_160.png", img2)
#dst = cv2.addWeighted(absX,0.5,absY,0.5,0)

elapsed = (time.clock() - start)
print("Time used:",elapsed)

#cv2.imshow("absX", absX)
cv2.imshow("absY", absY)
cv2.imshow("thresh", thresh)
thresh = cv2.resize(thresh, (160, 120), interpolation=cv2.INTER_AREA)
cv2.imwrite(("./angle_thresh_160.png"), thresh)

#cv2.imshow("Result", dst)
 
cv2.waitKey(0)
cv2.destroyAllWindows() 
