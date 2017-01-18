# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 11:50:41 2016

@author: Susie
"""

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Convolution2D,MaxPooling2D,Flatten
import pandas as pd
import numpy as np
from dateutil import parser
from keras.utils import np_utils
from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split

# from keras import backend as K

# K.softmax()
# load data
poseData = pd.read_csv("/Users/Susie/Downloads/PT29-48-w10-s4.csv", low_memory=False)

# omit NA
poseData = poseData[['accelerometerX','accelerometerY','accelerometerZ','groupId','q1','q3','q4','sms3']]

#group data and select the group which  # of row is 125
grouped = poseData.groupby('groupId')
# grouped = grouped.groupby(pd.TimeGrouper('2S'))
counts = grouped.size()
# have 108 groups of 2min data, split it into two groups, one for train is 0-90,rest is for test
X = poseData[['accelerometerX','accelerometerY','accelerometerZ','q1','q3','q4']]

grouped=grouped[['accelerometerX','accelerometerY','accelerometerZ','q1','q3','q4']]

X = X.as_matrix()
X = np.reshape(X,(2579,3750),order='C' )


'''
X_train = grouped.as_matrix()
X_train = X_train[0:11250,1:4]
X_train = X_train.astype('float32')


X_train = np.reshape(X_train, (90,1,625,6), order='C')

X_test = grouped.as_matrix()
X_test = X_test[11250:13500,1:4]
X_test = X_test.astype('float32')

X_test = np.reshape(X_test, (18,1,125,3), order='A')
'''
Y = poseData.groupby('groupId')
Y = Y.head(1)
Y = Y['sms3']

X,Y = shuffle(X,Y, random_state=2)
Y_train = Y[0:len(Y)*0.7]
Y_test = Y[len(Y)*0.7:]
    
# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(Y_train, nb_classes=3)
Y_test = np_utils.to_categorical(Y_test, nb_classes=3)
#here exist problem, the ideal result should be converted it to be a dummy sheet,but the result is all the same
# np_utils.to_categorical()

# number of output classes
nb_classes = 3

# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling (1,2)
# convolution kernel size (1,2)

model = Sequential()

model.add(Convolution2D(nb_filters, 1, 2,
                        border_mode='valid',
                        input_shape=(1, 125, 3)))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters, 1, 2))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(1, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(500))
model.add(Activation('softmax'))
model.add(Dropout(0.25))
model.add(Dense(nb_classes))
model.add(Activation('relu'))
model.compile(loss='categorical_crossentropy', optimizer='adadelta')

model.fit(X_test, Y_test, nb_epoch=5, batch_size=10, verbose=2)
scores = model.evaluate(X_test, Y_test)
# print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
