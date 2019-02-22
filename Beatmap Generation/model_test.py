'''Example script to generate text from Nietzsche's writings.
At least 20 epochs are required before the generated text
starts sounding coherent.
It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.
If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io
import Preprocessing
import json
from keras.models import load_model

path = get_file(
    'nietzsche.txt',
    origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
with open('Believer/Expert.json') as f:
    beatmap_json = json.load(f)
    text = Preprocessing.beeg_yoshi()
print('corpus length:', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
model = load_model('run3.h5')


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def create_pattern():
	start_index = random.randint(0, len(text) - maxlen - 1)
	for diversity in [2]:
	    output = ''
	    generated = ''
	    sentence = '    c      b      kj      fg      g'
	    generated += sentence

	    for i in range(5000):
	        x_pred = np.zeros((1, maxlen, len(chars)))
	        for t, char in enumerate(sentence):
	            x_pred[0, t, char_indices[char]] = 1.

	        preds = model.predict(x_pred, verbose=0)[0]
	        next_index = sample(preds, diversity)
	        next_char = indices_char[next_index]

	        generated += next_char
	        sentence = sentence[1:] + next_char

	        output += next_char
	return output