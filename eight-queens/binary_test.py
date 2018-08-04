import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("./pics/7.jpg")
#height, width = img.shape[:2]
img = cv2.resize(img,(300, 300), interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret2, th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#clear = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

kernel = np.ones((6,6),np.uint8)
erosion = cv2.erode(th2,kernel,iterations = 1)
#opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)
#dilation = cv2.dilate(th2,kernel,iterations = 1)
''' # Otsu's thresholding after Gaussian filtering
#（5,5）为高斯核的大小，0 为标准差
blur = cv2.GaussianBlur(gray,(5,5),0)
# 阈值一定要设为0！
ret1,th1 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
cv2.imshow("blur",blur) '''

''' th4 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
cv2.imshow("OTSU4",th4) '''

''' th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
cv2.imshow("adaptive",th3) '''
cv2.imshow("gray",gray)
cv2.imshow("OTSU2",th2)
cv2.imshow("erosion",erosion)
#cv2.imshow("dilation",dilation)
cv2.imwrite("./pics/7_bin.png",erosion)
cv2.waitKey(0)
cv2.destroyAllWindows()
