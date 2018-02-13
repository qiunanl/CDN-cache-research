from __future__ import print_function
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten,Activation
import numpy as np
from keras.models import load_model
import argparse
import cv2
import matplotlib
from matplotlib import pyplot as plt
from keras.optimizers import SGD
import scipy.io
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--save-model", type=int, default=-1,
	help="(optional) whether or not model should be saved to disk")
ap.add_argument("-l", "--load-model", type=int, default=-1,
	help="(optional) whether or not pre-trained model should be loaded")
ap.add_argument("-w", "--weights", type=str,
	help="(optional) path to weights file")
args = vars(ap.parse_args())

data = scipy.io.loadmat('hand_data')
xtrain = data["training"]
ytrain = data["train_label"]

model = Sequential()

# Architecture of Lenet-5: INPUT => CONV => RELU => POOL => CONV => RELU => POOL => FC => RELU => FC
# Convolution layer 1. Use 32 convolution filters
# Activation function is ReLU
# base experiment, without dropout and data augmentation
model.add(Conv2D(32, (3, 3), border_mode='valid', input_shape=xtrain.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# conv + relu + maxpooling
model.add(Conv2D(32, (3, 3), border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# fully connected layer
model.add(Flatten())
model.add(Dense(384))
model.add(Activation('relu'))

# fully connected layer
model.add(Dense(2))
model.add(Activation('softmax'))

batch_size = 100
epochs = 1

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

if args["load_model"] < 0:
     history = model.fit(xtrain, ytrain, batch_size=batch_size, epochs=epochs, verbose=1,
                     validation_data=(xtest, ytest))
     score = model.evaluate(xtest, ytest)
     print(score)

# check to see if the model should be saved to file
if args["save_model"] > 0:
 	print("[INFO] dumping weights to file...")
 	model.save_weights(args["weights"], overwrite=True)

model.save('lenet-5.h5')
