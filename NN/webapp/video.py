import cv2
import numpy as np
from tensorflow import keras
"""module contains class VideoCapwith method frame that gets frame and applies face detection and then emotion recognition. It returns modified frame(with recognition results added)."""


#Load Keras neural network for face recognition.
model = keras.models.load_model('webapp/cnn_face_recognition')
#List of emotions.
EMOTIONS_LIST = ["Angry", "Disgust",
                     "Fear", "Happy",
                     "Neutral", "Sad",
                     "Surprise"]

facec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCap(object):
    def __init__(self):
        #if cv2.VideoCapture(0).isOpened():
            #self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #else:
        self.video = cv2.VideoCapture('webapp/static/video1.avi')

    def __del__(self):
        self.video.release()

    def frame(self):
        goes, fr = self.video.read()
        if not goes:
             raise KeyError('end')
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h,x:x+w]

            roi = cv2.resize(fc, (48,48))
            pred = EMOTIONS_LIST[np.argmax(model.predict(roi[np.newaxis, :, :, np.newaxis]))]
            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
        _, jpeg = cv2.imencode('.jpg', fr)
        return goes, jpeg.tobytes()
