import pandas as pd
import numpy as np

from joblib import dump, load
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.model_selection import train_test_split

data = pd.read_csv('data_label.csv')

colsX = [col for col in data.columns if ('mean_mean' in col or 'min_mean' in col or 'max_mean' in col) and 'cloud' not in col]
colsY = ['Label_AH1N1', 'Label_AH3', 'Label_B']

dataX = data[colsX]
dataY = data[colsY]

trainX, valX, trainY, valY = train_test_split(dataX, dataY, train_size=0.8)

trainY_H1N1 = trainY['Label_AH1N1']
model_H1N1 = KNeighborsClassifier()
model_H1N1.fit(trainX, trainY_H1N1)
dump(model_H1N1, 'AH1N1.joblib')

trainY_H3 = trainY['Label_AH3']
model_H3 = KNeighborsClassifier()
model_H3.fit(trainX, trainY_H3)
dump(model_H3, 'AH3.joblib')

trainY_B = trainY['Label_B']
model_B = KNeighborsClassifier()
model_B.fit(trainX, trainY_B)
dump(model_B, 'B.joblib')


train_h1n1 = model_H1N1.score(trainX, trainY_H1N1)*100
train_h3 = model_H3.score(trainX, trainY_H3)*100
train_b = model_B.score(trainX, trainY_B)*100

test_h1n1 = model_H1N1.score(valX, valY['Label_AH1N1'])*100
test_h3 = model_H1N1.score(valX, valY['Label_AH3'])*100
test_b = model_H1N1.score(valX, valY['Label_B'])*100

print('================================== ACCURACY ===========================')
print('Accuracy on train set: AH1N1 - {}%, AH3 - {}%, B - {}%'.format(train_h1n1, train_h3, train_b))
print('-----------------------------------------------------------------------')
print('Accuracy on test set: AH1N1 - {}%, AH3 - {}%, B - {}%'.format(test_h1n1, test_h3, test_b))
print('=======================================================================')