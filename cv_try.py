#Python 2.7.2
#Opencv2 2.4.2
#PIL 1.1.7

import cv2 #Opencv2
import Image #Image from PIL
import glob
import os

def DetectFace(image, faceCascade, returnImage=False):
    # This function takes a grey scale cv2 image and finds
    # the patterns defined in the haarcascade function
    # modified from: http://www.lucaamore.com/?p=638

    #variables    
    min_size = (20,20)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0

    # Equalize the histogram
    cv2.EqualizeHist(image, image)

    # Detect the faces
    faces = cv2.HaarDetectObjects(
            image, faceCascade, cv2.CreateMemStorage(0),
            haar_scale, min_neighbors, haar_flags, min_size
        )

    # If faces are found
    if faces and returnImage:
        for ((x, y, w, h), n) in faces:
            # Convert bounding box to two cv2Points
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv2.Rectangle(image, pt1, pt2, cv2.RGB(255, 0, 0), 5, 8, 0)

    if returnImage:
        return image
    else:
        return faces

def pil2cv2Grey(pil_im):
    # Convert a PIL image to a greyscale cv2 image
    # from: http://pythonpath.wordpress.com/2012/05/08/pil-to-opencv2-image/
    pil_im = pil_im.convert('L')
    cv2_im = cv2.CreateImageHeader(pil_im.size, cv2.IPL_DEPTH_8U, 1)
    cv2.SetData(cv2_im, pil_im.tostring(), pil_im.size[0]  )
    return cv2_im

def cv22pil(cv2_im):
    # Convert the cv2 image to a PIL image
    return Image.fromstring("L", cv2.GetSize(cv2_im), cv2_im.tostring())

def imgCrop(image, cropBox, boxScale=1):
    # Crop a PIL image with the provided box [x(left), y(upper), w(width), h(height)]

    # Calculate scale factors
    xDelta=max(cropBox[2]*(boxScale-1),0)
    yDelta=max(cropBox[3]*(boxScale-1),0)

    # Convert cv2 box to PIL box [left, upper, right, lower]
    PIL_box=[cropBox[0]-xDelta, cropBox[1]-yDelta, cropBox[0]+cropBox[2]+xDelta, cropBox[1]+cropBox[3]+yDelta]

    return image.crop(PIL_box)

def faceCrop(imagePattern,boxScale=1):
    # Select one of the haarcascade files:
    #   haarcascade_frontalface_alt.xml  <-- Best one?
    #   haarcascade_frontalface_alt2.xml
    #   haarcascade_frontalface_alt_tree.xml
    #   haarcascade_frontalface_default.xml
    #   haarcascade_profileface.xml
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    imgList=glob.glob(imagePattern)
    if len(imgList)<=0:
        print 'No Images Found'
        return

    for img in imgList:
        pil_im=Image.open(img)
        cv2_im=pil2cv2Grey(pil_im)
        faces=DetectFace(cv2_im,faceCascade)
        if faces:
            n=1
            for face in faces:
                croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
                fname,ext=os.path.splitext(img)
                croppedImage.save(fname+'_crop'+str(n)+ext)
                n+=1
        else:
            print 'No faces found:', img

def test(imageFilePath):
    pil_im=Image.open(imageFilePath)
    cv2_im=pil2cv2Grey(pil_im)
    # Select one of the haarcascade files:
    #   haarcascade_frontalface_alt.xml  <-- Best one?
    #   haarcascade_frontalface_alt2.xml
    #   haarcascade_frontalface_alt_tree.xml
    #   haarcascade_frontalface_default.xml
    #   haarcascade_profileface.xml
    faceCascade = cv2.Load('haarcascade_frontalface_alt.xml')
    face_im=DetectFace(cv2_im,faceCascade, returnImage=True)
    img=cv22pil(face_im)
    img.show()
    img.save('test.png')


# Test the algorithm on an image
#test('testPics/faces.jpg')

# Crop all jpegs in a folder. Note: the code uses glob which follows unix shell rules.
# Use the boxScale to scale the cropping area. 1=opencv2 box, 2=2x the width and height
faceCrop('/home/prakkk/openface/test/class 1/*.jpg',boxScale=1)


