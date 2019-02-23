# BeatSaber Ogg Onset Detection
# 2/16/2019
# David Haas, Ian Boll, Josh Mosier, Michael Keays

import numpy as np
import h5py  # for saving the model
from tensorflow.python.lib.io import file_io  # for better file I/O
import tensorflow as tf
from datetime import datetime
import pickle
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
import argparse
import sys
import glob
#import cloud_datagen


def train_model(data_file='data/train120.pkl', job_dir='./tmp/onset_detect', epochs=10, **args):
    print(data_file, job_dir)
    # set the logging path for ML Engine logging to Storage bucket
    logs_path = job_dir + '/logs/' + datetime.now().isoformat()
    print('Using logs_path located at {}'.format(logs_path))

    f = tf.gfile.Open(data_file, mode="rb")
    data, labels = pickle.load(f)
    print("loaded")

    # Normalize the lengths of the data and labels for each song
    for i, ian in enumerate(zip(data, labels)):
        d, l = ian
        if l.shape[0] < d.shape[0]:
            diff = d.shape[0] - l.shape[0]
            labels[i] = np.concatenate(
                (labels[i], np.zeros(diff, dtype=np.bool)))
    print("normalized")

    training_cutoff = int(len(data) * .8)
    # Concatenate each song's data into a continuous list
    train_data = np.concatenate(data[:training_cutoff]).swapaxes(1, 3)
    test_data = np.concatenate(data[training_cutoff:]).swapaxes(1, 3)

    train_labels = np.concatenate(
        labels[:training_cutoff]).astype(np.short, copy=False)
    test_labels = np.concatenate(
        labels[training_cutoff:]).astype(np.short, copy=False)

    print("Data set.")

    from keras.models import Sequential
    from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout

    print("keras imported")

    # create model
    model = Sequential()

    # add model layers
    model.add(Conv2D(filters=10, kernel_size=(3, 7),
                     activation='relu', input_shape=(80, 15, 1)))
    model.add(MaxPooling2D(pool_size=(3, 1)))
    model.add(Conv2D(filters=10, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 1)))
    model.add(Flatten())
    model.add(Dense(256, activation='sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    model.add(Dropout(0.5))

    print("model created")

    model.compile(optimizer='adam',
                  loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    print("model compiled")

    model.fit(train_data, train_labels,
              validation_data=(test_data, test_labels),
              epochs=epochs)

    score = model.evaluate(test_data, test_labels, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    # Save the model to the Cloud Storage bucket's jobs directory
    with file_io.FileIO('model.h5', mode='r') as input_f:
        with file_io.FileIO(job_dir + '/model.h5', mode='w+') as output_f:
            output_f.write(input_f.read())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data-file',
        help='Cloud Storage bucket or local path to training data')
    parser.add_argument(
        '--job-dir',
        help='Cloud storage bucket to export the model and store temp files')
    parser.add_argument(
        '--epochs',
        help='Number of epochs to train the file over')
    args = parser.parse_args()
    arguments = args.__dict__

    # Parse the input arguments for common Cloud ML Engine options
    # if len(glob.glob('data/*.pkl')) == 0:
    #     job_dir = arguments['job_dir']
    #     if job_dir is None:
    #         job_dir = ''
    #     cloud_datagen.generate_data(
    #         'data/RawSongs/', 'data/train.pkl')

    # print(arguments)
    # train_model(**arguments)
    print(arguments)
    train_model(**arguments)


# model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)
