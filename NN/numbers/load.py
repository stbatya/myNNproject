import os
import struct
import numpy as np
import matplotlib.pyplot as plt

def load_mnist(path,kind='train'):
    """upload mnist DATA from path"""
    labels_path = os.path.join('D:/', 'NN', path,'%s-labels.idx1-ubyte' % kind)
    images_path = os.path.join('D:/', 'NN', path, '%s-images.idx3-ubyte' % kind)
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II', lbpath.read(8))
        labels = np.fromfile(lbpath, dtype=np.uint8)
    with open(images_path, 'rb') as imgpath:
        magic, n, rows, cols = struct.unpack('>IIII', imgpath.read(16))
        images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)
    return images, labels

X_train, y_train = load_mnist('numbers', kind='train')
#print('training rows: %d, columns %d'
        #% (X_train.shape[0],X_train.shape[1]))
#print(X_train[y_train == 9][0].reshape(28,28))
