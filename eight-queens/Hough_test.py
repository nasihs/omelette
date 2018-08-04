import cv2
import numpy as np


#import timeit
""" 
import time
start = time.clock()
 """
img = cv2.imread('./pics/32_bin.png')
img = cv2.resize(img,(300, 300), interpolation=cv2.INTER_AREA)

img = cv2.GaussianBlur(img,(3,3),0)
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img,50,150,apertureSize = 3)

#ret, tresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

lines = cv2.HoughLines(edges,1,np.pi/180,50)

#print (lines[0])
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    print (rho, theta)


#print (lines)
""" 
elapsed = (time.clock() - start)
print("Time used:",elapsed)
 """
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()