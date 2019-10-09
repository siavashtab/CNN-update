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

## Optimizer colleciton:
optzer = []
optzer_name = []
#-------------------------------------------------------------------------------
from keras.optimizers import Adam
##ref : https://arxiv.org/pdf/1412.6980v8.pdf
optzer.append(Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False))
optzer_name.append('Adam')
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
from keras.optimizers import SGD
optzer.append(SGD(learning_rate=0.01, momentum=0.0, nesterov=False))
optzer_name.append('SGD')
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
from keras.optimizers import RMSprop
## ref: http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf
optzer.append(RMSprop(learning_rate=0.001, rho=0.9))
optzer_name.append('RMSprop')
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
from keras.optimizers import Adagrad
## ref: http://www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf
optzer.append(Adagrad(learning_rate=0.01))
optzer_name.append('Adagrad')
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
from keras.optimizers import Adadelta
## ref: https://arxiv.org/pdf/1212.5701.pdf
optzer.append(Adadelta(learning_rate=1.0, rho=0.95))
optzer_name.append('Adadelta')
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
from keras.optimizers import Adamax
## ref: https://arxiv.org/pdf/1412.6980v8.pdf
optzer.append(Adamax(learning_rate=0.002, beta_1=0.9, beta_2=0.999))
optzer_name.append('Adamax')
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
from keras.optimizers import Nadam
## ref: http://cs229.stanford.edu/proj2015/054_report.pdf
optzer.append(Nadam(learning_rate=0.002, beta_1=0.9, beta_2=0.999))
optzer_name.append('Nadam')
#-------------------------------------------------------------------------------


seed = 7
np.random.seed(seed)

kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
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

model = Sequential()
model.add(Dense(256, activation='relu', input_dim=(32*32*3)))
model.add(Dense(256, activation='relu'))
model.add(Dense(10, activation='softmax'))

#### Loop over different optimizers
for algo in optzer:
    model.compile(optimizer=algo,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    history = model.fit(X_train.reshape(50000 , 32*32*3),to_categorical(y_train), epochs=15, batch_size=32, verbose=2, validation_split=0.2)
    score = model.evaluate(X_test.reshape(10000 , 32*32*3), to_categorical(y_test), batch_size=128)
    print(model.metrics_names)
    print(score)
    
    #MODEL SUMMARY AND PLOTS
    
    def summarize_diagnostics(history, optimizer):
        plt.subplot(211)
        plt.title('Cross Entropy Loss - Optimizer: ' + optimizer)
        plt.xlabel(' ')
        plt.ylabel(' ')
        plt.plot(history.history['loss'], color='blue', label='train')
        plt.plot(history.history['val_loss'], color='orange', label='test')
        plt.subplot(212)
        plt.title('Classification Accuracy - Optimizer: ' + optimizer)
        plt.xlabel(' ')
        plt.ylabel(' ')
        plt.plot(history.history['acc'], color='blue', label='train')
        plt.plot(history.history['val_acc'], color='orange', label='test')
    
    i = 1
    opttcount = 0
    for h in History:  
      summarize_diagnostics(h, optzer_name[opttcount ])
      plt.show()
      print('For Fold: ',i)
      print('-------------------------------------------------------------')
      i+=1
      opttcount += 1

