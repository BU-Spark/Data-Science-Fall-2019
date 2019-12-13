# --------------------------------------- load & split dataset ---------------------------------------
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def text_process(text):
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\S|@\S+', ' ', str(text))
    text = re.sub(r"n't", ' not', text)
    text = re.sub(r'[^A-Za-z0-9]+',' ',text)
    text = text.lower().strip()
    res = ''
    for token in text.split():
        if token not in stop_words:
            res = res + token + " "
    return res[: - 1]


def label_text_split(original_dataset):
    x = []
    y = []
    for data in original_dataset:
        x.append(data[5].lower())
        y.append([data[0]])
    return x, y


dataset = pd.read_csv("data/training.1600000.processed.noemoticon.csv", encoding = "ISO-8859-1").values.tolist()
stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")
for i in range(len(dataset)):
    dataset[i][5] = text_process(dataset[i][5])
train_set, test_set = train_test_split(dataset, test_size=0.2)
x_train, y_train = label_text_split(train_set)
x_test, y_test = label_text_split(test_set)

encoder = LabelEncoder()
encoder.fit(y_train)
y_train = encoder.transform(y_train)
y_test = encoder.transform(y_test)
y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)

# --------------------------------------- word2vec ---------------------------------------

from gensim.models import Word2Vec
import os

w2v_model_exists = os.path.isfile('model/w2v_model.w2v')
if w2v_model_exists:
    w2v_model = Word2Vec.load('model/w2v_model.w2v')
    print('w2v model loaded.')
else:
    w2v_model = Word2Vec(size=300, window=7, min_count=10, workers=8)
    sentences = [text.lower().split() for text in x_train]
    w2v_model.build_vocab(sentences, progress_per=10000)
    w2v_model.train(sentences, total_examples=len(sentences), epochs=30, report_delay=1)
    w2v_model.init_sims(replace=True)
    w2v_model.save('model/w2v_model.w2v')
    # w2v_model = Word2Vec.load('model/w2v_model.w2v')
    print('w2v model saved.')
print(w2v_model.wv.most_similar("happy"))


# --------------------------------------- train model ----------------------------------------------
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from keras.models import load_model

from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
import pickle

tokenizer = Tokenizer()
tokenizer.fit_on_texts(x_train)
vocab_size = len(tokenizer.word_index) + 1
print("Total words", vocab_size)

x_train = pad_sequences(tokenizer.texts_to_sequences(x_train), maxlen=300)
x_test = pad_sequences(tokenizer.texts_to_sequences(x_test), maxlen=300)

lstm_model_exists = os.path.isfile('model/lstm_model_5.h5')
if lstm_model_exists:
    lstm_model = load_model('model/lstm_model_5.h5')
    print('lstm model loaded.')
else:
    embedding_matrix = np.zeros((vocab_size, 300))
    for word, i in tokenizer.word_index.items():
        if word in w2v_model.wv:
            embedding_matrix[i] = w2v_model.wv[word]
    print(embedding_matrix.shape)

    embedding_layer = Embedding(vocab_size, 300, weights=[embedding_matrix], input_length=300, trainable=False)
    print(vocab_size, 300, 300)

    lstm_model = Sequential()
    lstm_model.add(embedding_layer)
    lstm_model.add(LSTM(128, return_sequences=True)) # returns a sequence of vectors of dimension 128
    lstm_model.add(LSTM(128))  # return a single vector of dimension 128
    lstm_model.add(Dense(1, activation='sigmoid'))

    lstm_model.summary()

    lstm_model.compile(loss='binary_crossentropy', optimizer="rmsprop", metrics=['accuracy'])

    callbacks = [ReduceLROnPlateau(monitor='val_loss', patience=5, cooldown=0),
                  EarlyStopping(monitor='val_acc', min_delta=1e-4, patience=5)]

    from keras.callbacks import CSVLogger

    csv_logger = CSVLogger('training.log', separator=',', append=False)
    history = lstm_model.fit(x_train, y_train,
                        batch_size=1024,
                        epochs=5,
                        validation_split=0.1,
                        verbose=1,
                        callbacks=callbacks)

    lstm_model.save('model/lstm_model_5 .h5')
    print('lstm model saved.')
    pickle_out = open("model/history.pickle","wb")
    pickle.dump(history.history, pickle_out)
    pickle_out.close()
    # lstm_model = load_model('model/lstm_model_without_dropput.h5')
    score = lstm_model.evaluate(x_test, y_test, batch_size=1024)
    print("ACCURACY:", score[1])
    print("LOSS:", score[0])


# --------------------------------------- predict ----------------------------------------------
def predict(text):
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=300)
    # Predict
    score = lstm_model.predict([x_test])[0]
    label = 0
    if score <= 0.4:
        label = -1
    elif score >= 0.7:
        label = 1
    return label


def predict_social_data(input_predict_filename, output_predict_filename):
    data = pd.read_csv(input_predict_filename)
    header = list(data.columns)
    print(header)
    text_column = -1
    for i in range(len(header)):
        if header[i] == 'text':
            text_column = i
    data = data.values.tolist()

    predict_score = []
    for item in data:
        text = str(item[text_column]).lower()
        score = predict(text)
        predict_score.append(score)

    df = pd.DataFrame(predict_score, columns=['score'])
    df.to_csv(output_predict_filename, index=True)
    print(len(data))


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


topics = ["arts", "community", "housing", "library", "program", "resident", "school", "service", "street", "youth"]
mkdir('predict_result')
for topic in topics:
    input_filename = 'twitter_mayor/' + topic + '.csv'
    output_filename = 'predict_result/' + topic + '_predict.csv'
    predict_social_data(input_filename, output_filename)
