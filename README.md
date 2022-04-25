# hw2-trade
hw2
目標: 預測股票走勢，並依走勢自動買進賣出

資料來源:
https://www.dropbox.com/s/uwift61i6ca9g3w/training.csv?dl=0
https://www.dropbox.com/s/duqiffdpcadu6s7/testing.csv?dl=0

利用今日開盤 預測明日開盤

先把將資料透過MinMaxScaler前處理，使得數據會縮放到到[0,1]之間

放入LSTM模型進行訓練

如果持有股票且開盤預測結果小於今日開盤，則賣出股票
如果未持有股票且開盤預測結果大於今日開盤，則買進股票
其他情況則不做任何動作
