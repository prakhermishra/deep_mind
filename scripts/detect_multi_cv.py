import cv2
import numpy as np

faceDetect = cv2.CascadeClassifier('/home/prakkk/Downloads/opencv-2.4.11/data/haarcascades/haarcascade_frontalface_default.xml');
#cam = cv2.VideoCapture(0);
count =0
img=cv2.imread('/home/prakkk/Downloads/classpicturesfortesting/prakhar_singhu.jpg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces= faceDetect.detectMultiScale(gray,1.3,5)
for(x,y,w,h) in faces:
	roi_img = img[y:y+h, x:x+w]
	print x,y,w,h
	image = "crop"+"{}".format(count)+".png"       
	cv2.imwrite(image,roi_img)
	count+=1
	if len(faces) == count:
		break

