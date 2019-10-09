# -*- coding: utf-8 -*-
"""cifar10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hvQQB0awUJf5zku5A5Z_GByf80C56hqD
"""

from keras.datasets import cifar10
from keras.layers import Dense , Conv2D ,  Flatten , MaxPool2D , BatchNormalization , Dropout
from keras.models import Sequential
from keras.utils import to_categorical
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#PREPROCESSING

(X_train , y_train) ,(X_test , y_test) = cifar10.load_data()
def custom_preprocess(data):
  data = data.astype('float')
  data /= 255.0
  return data
X_train  = custom_preprocess(X_train)
X_test = custom_preprocess(X_test)

plt.imshow(X_train[0])

X = np.vstack((X_train , X_test))
Y = np.vstack((y_train , y_test))
# Y = to_categorical(Y)
X[0].shape



from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score


seed = 7
np.random.seed(seed)
for nsplt in range(9):
    kfold = StratifiedKFold(n_splits=nsplt + 2, shuffle=True, random_state=seed)
    cvscores = []
    History = []
    F1_score = []
    for train, test in kfold.split(X, Y):
      
      model = Sequential()
      model.add( Conv2D(input_shape = (32, 32,3) , filters = 32 , kernel_size=(3,3) , padding = 'same' , activation = 'relu' , kernel_initializer= 'he_uniform'))
      model.add(BatchNormalization())
      model.add( Conv2D(filters = 32 , kernel_size = (3,3) , padding = 'same' , activation = 'relu' , kernel_initializer = 'he_uniform'))
      model.add( MaxPool2D(2,2))
      model.add( Dropout(0.2))
    
      model.add( Conv2D(filters = 64 , kernel_size = (3,3) , padding = 'same' , activation = 'relu' , kernel_initializer = 'he_uniform'))
      model.add(BatchNormalization())
      model.add( Conv2D(filters = 64 , kernel_size = (3,3) , padding = 'same' , activation = 'relu' , kernel_initializer = 'he_uniform'))
      model.add( MaxPool2D(2,2))
      model.add( Dropout(0.4))
    
      model.add( Conv2D(filters = 128 , kernel_size = (3,3) , padding = 'same' , activation = 'relu' , kernel_initializer = 'he_uniform'))
      model.add(BatchNormalization())
      model.add( Conv2D(filters = 128 , kernel_size = (3,3) , padding = 'same' , activation = 'relu' , kernel_initializer = 'he_uniform'))
      model.add( MaxPool2D(2,2))
      model.add( Dropout(0.5))
    
      model.add(Flatten())
      model.add(Dense(units = 128 , activation = 'relu' , kernel_initializer = 'he_uniform'))
      model.add(Dense(units = 10 , activation = 'softmax')) 
      model.compile(optimizer = 'adam' , loss = 'categorical_crossentropy' , metrics = ['accuracy'])
      History.append(model.fit(x = X[train], y = to_categorical(Y[train]) , epochs=50 , batch_size = 128 , validation_data=(X[test] , to_categorical(Y[test]))))
      scores = model.evaluate(X[test] , to_categorical(Y[test]))
      cvscores.append(scores[1] * 100)
      F1_score.append(f1_score( Y[test] ,  model.predict_classes(X[test]) , average = 'micro') )
     
    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
    
    # create data generator
    datagen = ImageDataGenerator(width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True)
    # prepare iterator
    it_train = datagen.flow(X_train, y_train, batch_size=64)
    
    # fit model
    steps = int(X_train.shape[0] / 64)
    history = model.fit_generator(it_train, steps_per_epoch=steps, epochs=100, validation_data=(testX, testY), verbose=0)
    
    print("Total Accuracy is %.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
    print("F1 Score is %.2f%% (+/- %.2f%%)" % (np.mean(F1_score), np.std(F1_score)))
    
    #USING MULTI LEVEL PERCEPTRON
    from keras.optimizers import Adam
    model = Sequential()
    model.add(Dense(256, activation='relu', input_dim=(32*32*3)))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    sgd = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
    
    model.compile(optimizer=sgd,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    history = model.fit(X_train.reshape(50000 , 32*32*3),to_categorical(y_train), epochs=15, batch_size=32, verbose=2, validation_split=0.2)
    score = model.evaluate(X_test.reshape(10000 , 32*32*3), to_categorical(y_test), batch_size=128)
    print(model.metrics_names)
    print(score)
    
    #MODEL SUMMARY AND PLOTS
    
    def summarize_diagnostics(history):
    	plt.subplot(211)
    	plt.title('Cross Entropy Loss')
    	plt.plot(history.history['loss'], color='blue', label='train')
    	plt.plot(history.history['val_loss'], color='orange', label='test')
    	plt.subplot(212)
    	plt.title('Classification Accuracy')
    	plt.plot(history.history['acc'], color='blue', label='train')
    	plt.plot(history.history['val_acc'], color='orange', label='test')
    
    i = 1
    for h in History:
      
      summarize_diagnostics(h)
      plt.show()
      print('For Fold: ',i)
      print('-------------------------------------------------------------')
      i+=1

