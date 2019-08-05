import numpy as np
import cv2


face_cascade = cv2.CascadeClassifier('cascade.xml')
img = cv2.imread('Training/show_img/1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)

faces = face_cascade.detectMultiScale(gray, 
                                      scaleFactor = 1.1, 
                                      minNeighbors = 5, 
                                      minSize = (24, 24))

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

cv2.imwrite("img_show_1.png", img)

