import nltk
nltk.download('punkt')
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import pandas as pd

df = pd.read_csv("CNN_Articels_clean.csv")
print(df.head())


words = nltk.tokenize.word_tokenize(df.loc[0, 'Article text'])
print(words[0:100])

vocab_size = 10000
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts([words])
encoded = tokenizer.texts_to_sequences([words])[0]
print(encoded[:100])

inputlengh = 5

sequences = list()
for i in range(inputlengh, len(encoded)):
    sequence = encoded[i-inputlengh:i+1]
    sequences.append(sequence)
print('Total Sequences: %d' % len(sequences))

sequences = np.array(sequences)
X, y = sequences[:,:inputlengh],sequences[:,inputlengh]
Xlen = len(X)
print(X[:10,:])
print(y[:10])

model = Sequential()
model.add(Embedding(vocab_size, 300, input_length=inputlengh))
model.add(LSTM(150, return_sequences=True))
model.add(LSTM(75))
model.add(Dense(vocab_size, activation='softmax'))
print(model.summary())

def generator(features, labels, batch_size):
    X_batch = np.zeros((batch_size, inputlengh))
    y_batch = np.zeros((batch_size,vocab_size))

    while True:
        for i in range(batch_size):
            index = random.randint(0, Xlen-1)
            X_batch[i] = features[index]
            y_batch[i] = to_categorical(labels[index], num_classes=vocab_size)
        yield X_batch, y_batch


my_generator = generator(X,y,1000)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit_generator(my_generator, steps_per_epoch = 3, epochs=5, verbose=2)

def generate_seq(model, tokenizer, seed_text, n_words):
    textlist = seed_text.split()
    in_text, result = textlist[-5:], seed_text
    for _ in range(n_words):      
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        encoded = pad_sequences([encoded], maxlen=inputlengh, padding='pre')
    
        probs = model.predict_ (encoded)
        yhat = random.choices(range(0,vocab_size), weights=probs[0], k=1)[0]
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
        in_text, result = out_word, result + ' ' + out_word
    return result

print(generate_seq(model, tokenizer, 'There is a stark shortage of workers since the pandemic', 100))