from flask import Blueprint
from flask import Flask
from flask import render_template, request, jsonify
import base64
import numpy as np
import cv2
import pickle
from tensorflow import keras
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


#with open(f'model_nn.pkl', 'rb') as f:
        #model = pickle.load(f)
model = keras.models.load_model('webapp/cnn_model')

@main.route('/')
def index():
    return render_template('index.html', name='K')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.name)

@main.route('/canvas', methods = ['GET','POST'])
def canvas():
    if request.method == 'POST':
        #print('accepted')
        #print(request.json['data'])
        draw = request.json['data'].split(',')[1]
        #print(draw)
        #print('code_ended')
        draw_decoded = base64.b64decode(draw)
        image = np.asarray(bytearray(draw_decoded), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        #Resizing and reshaping to keep the ratio.
        resized = cv2.resize(image, (28,28), interpolation = cv2.INTER_AREA)
        x_vector = np.asarray(resized, dtype="uint8")
        x_vector = x_vector.reshape(1,784)
        for i in range(784):
            x_vector[0][i]=255*x_vector[0][i]/(x_vector[0][i]+1)
        print(x_vector.reshape(28,28))
        x_vector = x_vector.reshape(1,28,28,1)
        y_pred = model.predict(x_vector)
        pred = int(np.argmax(y_pred))
        print(pred)
        return jsonify({'result':pred})
    return render_template('canvas.html', msg = 'get')
