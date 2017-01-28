# https://github.com/fchollet/keras/blob/master/examples/lstm_text_generation.py

# Standard library
import os
from os.path import exists, join, abspath, dirname
import random
import json

# Third-party
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
import numpy as np

maxlen = 48
temp = 0.5

def get_model(maxlen, chars):
    # build the model: 2 stacked LSTM
    print('Build model...')
    model = Sequential()
    model.add(LSTM(512, return_sequences=True,
                   input_shape=(maxlen, len(chars))))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(len(chars)))
    model.add(Activation("softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

    return model

def sample(seed, nchars):

    weights_file = abspath(os.environ['WEIGHTSPATH'])
    cache_path = dirname(weights_file)
    char_indices_file = join(cache_path, 'char_indices.json')
    corpus_file = join(cache_path, 'corpus.txt')

    with open(char_indices_file) as f:
        d = json.loads(f.read())
        chars = d['chars']
        char_indices = d['char_indices']
        indices_char = d['indices_char']

    with open(corpus_file) as f:
        text = f.read().lower()

    model = get_model(maxlen, chars)
    model.load_weights(weights_file)

    def sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    generated = ""
    start_index = random.randint(0, len(text) - maxlen - 1)

    # find whitespace closest to start index
    for i in range(128):
        if text[start_index] != ' ':
            start_index += 1
    start_sentence = text[start_index: start_index + maxlen]
    generated += start_sentence

    ngenerated = 0
    niter = 0
    maxiter = nchars * 2
    break_next = False
    sentence = start_sentence
    while niter < maxiter:
        x = np.zeros((1, maxlen, len(char_indices)))
        for t, char in enumerate(sentence):
            x[0, t, char_indices[char]] = 1.

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, temp)
        next_char = indices_char[str(next_index)]
        generated += next_char
        sentence = sentence[1:] + next_char

        ngenerated += 1
        if ngenerated >= nchars:
            break_next = True # finish sentence, then break

        if next_char == '.' and break_next:
            break

    return generated
