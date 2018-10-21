# go WC = 0  3 = 1  walk = 2  run = 3 occupied = 4   walk and run = 5  eating = 6  driving = 7
import json
import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
import keras.preprocessing.text as kpt
from keras.layers import Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split

np.random.seed(1337)
data = pd.read_csv("./Training_data/training_data.csv")
data.info(memory_usage='deep')
x = data[['heart_rate','tidal_volume_adjusted','cadence','step','activity','NN_interval','temperature_celcius']]
y = data['Activity'] = pd.to_numeric(data['Activity'], errors='coerce')
print( np.unique(y))
print(data[pd.to_numeric(data['Activity'], errors='coerce').isnull()])

model = Sequential()
model.add(Dense(512, input_shape=(7,), activation='relu'))
model.add(Dropout(0.7))

model.add(Dense(512, activation='relu'))
model.add(Dropout(0.7))

model.add(Dense(512, activation='relu'))
model.add(Dropout(0.7))

model.add(Dense(512, activation='relu'))
model.add(Dropout(0.7))

model.add(Dense(512, activation='relu'))
model.add(Dropout(0.7))

model.add(Dense(2, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

filepath = 'model_sentiment.h5'
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.20, random_state=42, shuffle=True)
# Fit the model
hist = model.fit(X_train, Y_train, validation_split=0.20, epochs=25, batch_size=32, callbacks=callbacks_list, verbose=1)
# Evaluate the model
loss, accuracy = model.evaluate(X, Y, verbose=0)
print('Accuracy: %f' % (accuracy * 100))
print('***** TOTAL TRAINING SET AMOUNT', X_train.shape, Y_train.shape)
print('***** TEST', X_test.shape, Y_test.shape)
print(model.summary())

# Show chart(s)
loss = hist.history['loss']
val_loss = hist.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'b', label='Training loss', linestyle='solid')
plt.plot(epochs, val_loss, 'r', label='Validation loss', linestyle='solid')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid(True)
plt.legend()
plt.style.use(['classic'])
plt.show()

train_acc = hist.history['acc']
val_acc = hist.history['val_acc']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'b', label='Training loss', linestyle='solid')
plt.plot(epochs, train_acc, 'g', label='Training Accuracy', linestyle='solid')
plt.plot(epochs, val_acc, 'r', label='Validation Accuracy', linestyle='solid')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.grid(True)
plt.legend()
plt.style.use(['classic'])
plt.show()
