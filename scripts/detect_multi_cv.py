import cv2
import numpy as np
import time
import subprocess
import os
import random
import Queue as Q
from threading import Thread
import sentiment_api as sap

faceDetect = cv2.CascadeClassifier('/home/prakkk/Downloads/opencv-2.4.11/data/haarcascades/haarcascade_frontalface_default.xml');
#cam = cv2.VideoCapture(0);
count = 0
session = 0
def crop_images(image):
	global count
	global session
	session +=1
	#print 'called'
	#img=cv2.imread('/home/prakkk/Downloads/classpicturesfortesting/prakhar_singhu.jpg')
	img = image
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces= faceDetect.detectMultiScale(gray,1.3,5)
	for(x,y,w,h) in faces:
		cv2.imshow('img',img)
		roi_img = img[y:y+h, x:x+w]
		
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		#print x,y,w,h
		#image = "crop"+"{}".format(count)+".png"
		image = str(random.randint(1,100))+str(unichr(random.randint(65,90)))+".png"		
		#cv2.imshow('crop',roi_img)
		#print image    
		path = '/home/prakkk/galgotia-hack/data/sentiment/test/'
		w = path+image
		print w   
		cv2.imwrite(w,roi_img)
		#count+=1
		
		p = subprocess.Popen("./infer.sh %s" % (str(image)), stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		l1 = output.split(" ")
		try:
			person_id = l1[3]
			print 'hua'
			print person_id
			#os.system('chmod 777 -R /home/prakkk/galgotia-hack/data/sentiment/')
			try:
				os.stat('/home/prakkk/galgotia-hack/data/sentiment/'+str(session)+'/'+person_id)
			except:
				os.makedirs('/home/prakkk/galgotia-hack/data/sentiment/'+str(session)+'/'+person_id)
			subprocess.Popen("./move.sh %s %s %s" % (str(person_id),str(image),str(session)), stdout=subprocess.PIPE, shell=True)
			#subprocess.call(['./move.sh %s %s' % (str(person_id),str(image))])
			#print person_id
			#if len(faces) == count:
			#	break
		except:
			print 'nahi hua recog'
	#for subdir, dirs, files in os.walk(rootdir):
	#	for file in files:
	#		print os.path.join(subdir, file)
q=Q.Queue()
flag=True
def display():
	global count
	cap = cv2.VideoCapture(0)
	#cap_display = cv2.VideoCapture(0)
	while 1:
		ret, img = cap.read()
		#ret1,img1 = cap_display.read()
		if ret: 
			if count%100 ==0:
				q.put(img)
			else:
				cv2.imshow('img',img)
			#time.sleep(3)			
		else:
			print "unable to load"
			break
		count+=1
		#cv2.imshow('img',img)
		k = cv2.waitKey(30) & 0xff
		if k == 27:
			break
	cap.release()
	cv2.destroyAllWindows()

def process_frame():
	while 1:
		try:
			crop_images(q.get())
		except:
			pass
def update():
	print 'chal gya'
	rootdir = '/home/prakkk/galgotia-hack/data/sentiment/'
	l=[]
	directory = []
	f1 =[]
	for subdir, dirs, files in os.walk(rootdir):
		for f in files:
			l.append(os.path.join(subdir,f))
		for d in dirs:
			directory.append(d)	

	for s in l:
		print s
		#print s.split('/')[6]
		if s.split('/')[6] == 'test' or s.split('/')[6] == 'result.json' or s.split('/')[6] == 'result.json~' or s.split('/')[6] == 'result1.json' or s.split('/')[6] == 'result1.json~':
			#print 'abc'
			pass
		else:
			print s
			s1 = '/'+s.split('/')[6]+'/'+s.split('/')[7]+'/'+s.split('/')[8]
			sap.callPath(s1,s.split('/')[6],s.split('/')[7])
			f1.append(s)



thread1 = Thread(target = display)
thread1.start()

thread2 = Thread(target = update)
thread2.start()



while flag:
	if(flag and q.qsize()>0):
		flag = False
		process_frame().start()
		
