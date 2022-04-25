# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 22:32:22 2022

@author: USER
"""

if __name__ == '__main__':
    #import packages
    import argparse
    import csv
    import pandas as pd
    import numpy as np
    from keras.models import Sequential
    from keras.layers import LSTM, Dense, Activation
    from sklearn.preprocessing import MinMaxScaler

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args(args=[])
    
    
    #read training data
    train = pd.read_csv("training.csv", usecols = [0])
    train = train.values
    train = train.astype('float32')
    
    #read testing data
    test = pd.read_csv("testing.csv", usecols = [0])
    test = test.values
    test = test.astype('float32')
    
    # Normalize 資料
    MMS = MinMaxScaler(feature_range= (0, 1))
    
    train = MMS.fit_transform(train)
    test = MMS.fit_transform(test)
    
    train_X , train_Y = [], []
    
    #x為昨日數據 ,y為今日數據
    for i in range(len(train)-1):
        train_X.append(train[i])
        train_Y.append(train[i+1])
        
        
    train_x = np.array(train_X)
    train_y = np.array(train_Y)
    test = np.array(test) 
    
    #build LSTM & train
    model = Sequential()
    model.add(LSTM(4, input_shape=(1, 1)))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss = 'MSE', optimizer = 'adam')
    model.fit(train_x, train_y, epochs = 10)
    
    hold = False  #是否持有股票
    output = []
    
    for i in range(19):
        predict = model.predict(test[:i+1])
        
        #沒股票且預測明日結果>今日，買進
        if ((not hold) and (predict[-1, 0] > test[i, 0])):
            hold = True
            output.append(1)
        #有股票且預測明日結果<今日，賣出    
        elif (hold and predict[-1, 0] > test[i, 0]):
            hold = False
            output.append(-1)
            
        else:
            output.append(0)
            
    #寫入答案        
    with open(args.output, 'w') as output_file:
        
        writer = csv.writer(output_file)
        
        for i in range(19):
            writer.writerow([f"{i}", output[i]])
        
        
    