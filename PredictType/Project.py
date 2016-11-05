'''
Predicts upcoming crime type using last look_back crime types
'''
import numpy
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

'''
SHAPE THE DATASET
'''

numpy.random.seed(7)

dataframe = numpy.loadtxt("Kingston_Police_Formatted.csv",delimiter=",")
train_size = int(len(dataframe)*0.67) #length of 2/3rds into the dataset
test_size = int(len(dataframe)-train_size) #length 1/3rd of the dataset

#2D arrays, subsets of dataframe containing only first 6 elements of each entry
train = dataframe[0:train_size,:6]
test = dataframe[train_size:len(dataframe),:6]
train_main = dataframe[0:train_size,:6]
test_main = dataframe[train_size:len(dataframe),:6]

def create_database(dataset,look_back=1):
    #3D arrays, len(dataset) X number of datapoints X features per datapoint
    dataX = [] #datapoints are arrays containing last look_back crime types
    dataY = [] #datapoints are the upcoming crime type

    for i in range(len(dataset)-look_back-1):
        dataX.append(dataset[i:(i+look_back),:])
        dataY.append(dataset[i+look_back,:])
    
    return numpy.array(dataX), numpy.array(dataY)

trainX_main, trainY_main = create_database(train_main,4)
testX_main, testY_main = create_database(test_main,4)

trainX_main = numpy.reshape(trainX_main,(trainX_main.shape[0],4,6))
testX_main = numpy.reshape(testX_main,(testX_main.shape[0],4,6))

'''
RUN THE NEURAL NET
'''

model=Sequential()
model.add(LSTM(32,input_dim=6))
model.add(Dense(6))
model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(trainX_main, trainY_main, nb_epoch=10,batch_size=10, verbose=2)

score = model.evaluate(testX_main,testY_main,batch_size=10)

print(score)

model.save('my_modeltest.h5')