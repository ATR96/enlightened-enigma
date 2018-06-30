import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout, GRU, CuDNNGRU
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.text import one_hot
import pickle
import heapq

np.random.seed(47)
path = "in1.txt"
rawtxt = open(path).read().lower()

chars = sorted(list(set(rawtxt)))
vocab = len(chars)

char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))

print"Unique Chars: ", vocab
print "Raw Data: ", len(rawtxt)

sequence_len = 17

def get_sequence(rawtxt, chars, sequence_len):

	datas=rawtxt.split("~")
	sentences = []
	next_chars = []

	for data in datas:

		if len(list(data)) > 6:

			#print data
			continue

		for i in range(0, len(data), 2):
			sentences.append(data[:i])
			next_chars.append(data[i])

	print('num training examples: ',len(sentences))

	x = one_hot(sentences)
	y = one_hot(next_chars)

	# x = np_utils.to_categorical(sentences)
	# y = np_utils.to_categorical(next_chars)

		
	# x = np.zeros((n_patterns, sequence_len, len(chars)), dtype=np.bool)

	# y = np.zeros((n_patterns, len(chars)), dtype=np.bool)

	# for i, sentence in enumerate(datax):

	# 	for t, word in enumerate(sentence):

	# 		x[i, t, word] = 1

	# for i, w in enumerate(datay):

	# 	y[i, w] = 1



	return x, y

x, y = get_sequence(rawtxt, chars, sequence_len)
#print (x.shape, '\n', y.shape)

model = Sequential()

model.add(GRU(128, input_shape=(sequence_len, vocab)))
model.add(Dense(vocab, activation = 'softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

filepath = "wt-imp5.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor = 'loss', verbose = 1, save_best_only = True, mode = 'min')
callbacks_list = [checkpoint]

x, y, n = get_sequence(rawtxt, chars, sequence_len)

history = model.fit(x, y, epochs = 1, validation_split = 0.05,  batch_size = 500, callbacks = callbacks_list, shuffle=True).history

model.save('keras_model5.h5')
pickle.dump(history, open("history5.p", "wb"))
