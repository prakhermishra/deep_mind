import cv2, sys, numpy, os
import dlib
from skimage import io
import json
import uuid
import random
from datetime import datetime
from random import randint
#predictor_path = sys.argv[1]
fn_haar = 'haarcascade_frontalface_default.xml'
fn_dir = 'att_faces'
size = 4
detector = dlib.get_frontal_face_detector()
#predictor = dlib.shape_predictor(predictor_path)
options=dlib.get_frontal_face_detector()
options.num_threads = 4
options.be_verbose = True

win = dlib.image_window()

# Part 1: Create fisherRecognizer
print('Training...')

# Create a list of images and a list of corresponding names
(images, lables, names, id) = ([], [], {}, 0)

for (subdirs, dirs, files) in os.walk(fn_dir):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(fn_dir, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1

(im_width, im_height) = (112, 92)

# Create a Numpy array from the two lists above
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

# OpenCV trains a model from the images

model = cv2.createFisherFaceRecognizer(0,500)
model.train(images, lables)

haar_cascade = cv2.CascadeClassifier(fn_haar)
webcam = cv2.VideoCapture(0)
webcam.set(5,30)
while True:
    (rval, frame) = webcam.read()
    frame=cv2.flip(frame,1,0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mini = cv2.resize(gray, (gray.shape[1] / size, gray.shape[0] / size))

    dets = detector(gray, 1)

    print "length", len(dets)

    print("Number of faces detected: {}".format(len(dets)))
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            i, d.left(), d.top(), d.right(), d.bottom()))

    cv2.rectangle(gray, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 3)


    '''
        #Try to recognize the face
        prediction  = model.predict(dets)
        print "Recognition Prediction" ,prediction'''





    win.clear_overlay()
    win.set_image(gray)
    win.add_overlay(dets)

if (len(sys.argv[1:]) > 0):
    img = io.imread(sys.argv[1])
    dets, scores, idx = detector.run(img, 1, -1)
    for i, d in enumerate(dets):
        print("Detection {}, score: {}, face_type:{}".format(
            d, scores[i], idx[i]))


