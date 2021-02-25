from flask import Blueprint
from flask import Flask
from flask import render_template, request, jsonify
import base64
import numpy as np
import cv2
import pickle
from tensorflow import keras
from flask_login import login_required, current_user
from .models import User, Result
from webapp import db
from sqlalchemy import select

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
    table = db.session.query(Result).filter_by(person_id=current_user.get_id()).all()
    imglist = []
    for item in table:
        img = pickle.loads(item.picture)
        img = img.reshape(28,28)
        #print(img.shape)
        retval, img = cv2.imencode('.jpg', img)
        #cv2.imshow('img', img)
        item.picture = str(base64.b64encode(img),'utf-8').strip()
        print(item.picture)
        #imglist.append(base64.b64encode(img[0][:][:][0]))
    #print(result)
    return render_template('profile.html', name = current_user.name, table=table)

@main.route('/canvas', methods = ['GET','POST'])
def canvas():
    if request.method == 'POST':
        #print('accepted')
        #print(request.json['data'])
        draw = request.json['data'].split(',')[1]
        #print(draw)
        #print('code_ended')
        #print('base64is!',draw)
        draw_decoded = base64.b64decode(draw)
        #print('decodedis!',draw_decoded)
        image = np.asarray(bytearray(draw_decoded), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        #Resizing and reshaping to keep the ratio.
        resized = cv2.resize(image, (28,28), interpolation = cv2.INTER_AREA)
        x_vector = np.asarray(resized, dtype="uint8")
        x_vector = x_vector.reshape(1,784)
        for i in range(784):
            x_vector[0][i]=255*x_vector[0][i]/(x_vector[0][i]+1)
        #print(x_vector.reshape(28,28))
        x_vector = x_vector.reshape(1,28,28,1)
        y_pred = model.predict(x_vector)
        pred = int(np.argmax(y_pred))
        if current_user.is_authenticated:
            pict = pickle.dumps(x_vector)
            new_digit = Result(picture = pict, prediction = pred, person_id = current_user.get_id())
            db.session.add(new_digit)
            db.session.commit()
        #print(pred)
        return jsonify({'result':pred})
    return render_template('canvas.html', msg = 'get')
