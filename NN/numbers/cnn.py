import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow

from keras.models import Model, Sequential
from keras.layers import *
from keras.preprocessing.image import array_to_img, img_to_array
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from load import load_mnist
from sklearn.model_selection import train_test_split


X_train, y_train = load_mnist('numbers', kind='train')
X_test, y_test = load_mnist('numbers', kind='t10k')

X_train = X_train.reshape((X_train.shape[0]), 28, 28, 1)
X_test = X_test.reshape((X_test.shape[0]), 28, 28, 1)

datagen = ImageDataGenerator(
        featurewise_center=False,
        samplewise_center=False,
        featurewise_std_normalization=False,
        samplewise_std_normalization=False,
        zca_whitening=False,
        rotation_range=20,
        zoom_range = 0.2,
        width_shift_range=0.15,
        height_shift_range=0.15,
        horizontal_flip=False,
        vertical_flip=False)

datagen.fit(X_train)

result_data = datagen.flow(X_train[0:5], y_train[0:5], batch_size=128)
x = result_data.next() #fetch the first batch
a = x[0] # train data
b = x[1] # train label
for i in range(0, 5):
    plt.imshow(a[i])
    plt.title(b[i])
    plt.show()


y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu',))
model.add(MaxPooling2D((2,2)))
model.add(SeparableConv2D(64, (3, 3), activation='relu',))
model.add(SeparableConv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2,2)))
model.add(Dropout(0.25))
model.add(BatchNormalization())
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(10, activation='softmax'))
opt = keras.optimizers.SGD(lr=0.01, momentum=0.9)
model.compile(optimizer=opt, loss ='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(datagen.flow(X_train, y_train, batch_size=128), epochs=25, validation_data=(X_test, y_test))

model.save('cnn_model')

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
