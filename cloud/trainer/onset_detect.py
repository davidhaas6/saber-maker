# BeatSaber Ogg Onset Detection
# 2/16/2019
# David Haas, Ian Boll, Josh Mosier, Michael Keays

import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout

# create model
model = Sequential()

# add model layers
model.add(Conv2D(filters=10, kernel_size=(7, 3),
                 activation='relu', input_shape=(80, 15, 1)))
model.add(MaxPooling2D(pool_size=(3, 1)))
model.add(Conv2D(filters=10, kernel_size=(7, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 1)))
model.add(Flatten())
model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.add(Dropout(0.5))

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])

#model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)
