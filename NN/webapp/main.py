"""Module that contains blueprints for basic pages"""


from flask import Blueprint
from flask import Flask
from flask import render_template, request, jsonify, Response
import base64
import numpy as np
import cv2
import pickle
from tensorflow import keras
from flask_login import login_required, current_user
from .models import User, Result
from webapp import db
from sqlalchemy import select
from .video import VideoCap


#Set a flask blueprint.
main = Blueprint('main', __name__)

#Load keras model for digit recognition.
model = keras.models.load_model('webapp/cnn_model')


@main.route('/')
def index():
    """Route for main page"""
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    """Route for profile page"""

    #Query to get logged user's data.
    table = db.session.query(Result).filter_by(
        person_id=current_user.get_id()).all()
    imglist = []

    #Loop through query rows.
    for item in table:

        #Load picture from 'picture' column (it was packed using pickle).
        #At this moment the picture is numpy array.
        img = pickle.loads(item.picture)

        #Reshape the picture.
        img = img.reshape(28,28)

        #Encode numpy array as jpeg picture.
        retval, img = cv2.imencode('.jpg', img)

        #Encode picture to base64.
        #On frontend side it will be dealt with as base64 image in <img> tag.
        item.picture = str(base64.b64encode(img),'utf-8').strip()
    return render_template('profile.html', name=current_user.name, table=table)


@main.route('/canvas', methods = ['GET','POST'])
def canvas():
    """Route for page with canvas for painting"""
    if request.method == 'POST':

        #Get the json request.
        #The picture in base64 is the part of string after comma.
        draw = request.json['data'].split(',')[1]

        #Decode base64.
        draw_decoded = base64.b64decode(draw)

        #Get picture as numpy array.
        image = np.asarray(bytearray(draw_decoded), dtype="uint8")

        #Code it as a grayscale.
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

        #Resize and reshape to 28x28.
        resized = cv2.resize(image, (28,28), interpolation=cv2.INTER_AREA)

        #Back to numpy.
        x_vector = np.asarray(resized, dtype="uint8")

        #Reshape to 28*28=784 dimensional vector.
        x_vector = x_vector.reshape(1,784)

        #Scale vector coordinates to [0;1] interval.
        for i in range(784):
            x_vector[0][i] = 255 * x_vector[0][i] / (x_vector[0][i] + 1)

        #Add dimensions to match neural network input.
        x_vector = x_vector.reshape(1,28,28,1)

        #Make a prediction with model.
        y_pred = model.predict(x_vector)

        #Get an integer mark of predicted class.
        pred = int(np.argmax(y_pred))

        #If user is authenticated dump the image with pickle
        #and add image and prediction to the Result table.
        if current_user.is_authenticated:
            pict = pickle.dumps(x_vector)
            new_digit = Result(picture=pict, prediction=pred,
                                person_id=current_user.get_id())
            db.session.add(new_digit)
            db.session.commit()

        #Return prediction.
        return jsonify({'result':pred})
    return render_template('canvas.html', msg='get')


def gen(camera):
    """Generator that yields video frame by frame"""
    while True:

        #Try to get a next frame of videostream and yield it.
        try:
            goes, frame = camera.frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #If out of frames then return.
        except KeyError:
            return


@main.route('/video_feed')
def video_feed():
    """Route for video feed.

    Returns a response with result of Camera generator applied to VideoCap.
    """
    
    #Specifies mimetype also.
    return Response(gen(VideoCap()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route('/face')
def face():
    """Route for page with facial emotions recognition"""
    return render_template('face.html')
