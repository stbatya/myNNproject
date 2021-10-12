"""module contains class VideoCap with method frame that
gets frame and applies face detection and then emotion recognition.

This object returns modified frame(with recognition results added).
"""


import cv2
import numpy as np
from tensorflow import keras


#Load Keras neural network for face recognition.
model = keras.models.load_model('webapp/cnn_face_recognition')

#List of emotions.
EMOTIONS_LIST = ["Angry", "Disgust",
                     "Fear", "Happy",
                     "Neutral", "Sad",
                     "Surprise"]

#Haar classifier for face detection.
facec = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#Set font.
font = cv2.FONT_HERSHEY_SIMPLEX


class VideoCap(object):
    """Class instances are video objects.

    Frame method yields next frame or raises key error at the end of the video.
    """

    def __init__(self):
        self.video = cv2.VideoCapture("webapp/static/video1.mp4")

    def __del__(self):
        self.video.release()

    def frame(self):
        """Uses VideoCapture read() method to get the next frame.
        Does face detection and emotion recognition.

        Raises KeyError when out of frames.

        Returns frame with added prediction.
        """

        goes, fr = self.video.read()

        #If none frame was read then we are at the end of the video.
        if not goes:
             raise KeyError('end')

        #Transform frame to grayscale.
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)

        #Use haar classifier to detect face on a frame.
        #It will return a list of rectangles.
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        #Looping through rectangles in list.
        for (x, y, w, h) in faces:

            #Taking the part of grayscaled frame that is inside the rectangle.
            fc = gray_fr[y:y+h,x:x+w]

            #Convert it to 48x48 to match Neutral network input dimensions.
            roi = cv2.resize(fc, (48,48))

            #Get the prediction.
            pred = EMOTIONS_LIST[np.argmax(model.predict(
                roi[np.newaxis, :, :, np.newaxis]))]

            #Put a text with prediction and draw a rectangle around the recognised face.
            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

        #Encode image as jpg and return it as bytes.
        _, jpeg = cv2.imencode('.jpg', fr)
        return goes, jpeg.tobytes()
