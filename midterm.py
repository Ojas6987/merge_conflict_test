# -*- coding: utf-8 -*-
"""midterm

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ODC7yD3LqSISzVffk1_hNP-su_WVMk3p
"""

import json
import gzip
import math
import numpy as np
from collections import defaultdict
from sklearn import linear_model
import random
import statistics

#MAKING A CHANGE IN FHTE FILE LFGGGGGGLFGGGGGLGGGGG


#MADE ANOTHER FUCKING COMMENT LFG

def assertFloat(x):
    assert type(float(x)) == float

def assertFloatList(items, N):
    assert len(items) == N
    assert [type(float(x)) for x in items] == [float]*N

answers = {}

# From https://cseweb.ucsd.edu/classes/fa24/cse258-b/files/steam.json.gz
z = open("train.json")

dataset = []
for l in z:
    d = eval(l)
    dataset.append(d)

z.close()

### Question 1

len(dataset)

def MSE(y, ypred):
    return np.mean((np.array(y)-np.array(ypred))**2)

def feat1(d):
  return [1] + [len(d['text'])]

X = [feat1(i) for i in dataset]
y = [i['hours'] for i in dataset]

from sklearn.linear_model import LinearRegression

mod = LinearRegression()
mod.fit(X, y)

yhat = mod.predict(X)
mse1 = MSE(y, yhat)

mse1



answers['Q1'] = [float(mod.coef_[1]), float(mse1)] # Remember to cast things to float rather than (e.g.) np.float64

assertFloatList(answers['Q1'], 2)

### Question 2

dataTrain = dataset[:int(len(dataset)*0.8)]
dataTest = dataset[int(len(dataset)*0.8):]



under = 0
over = 0

Xtrain = [feat1(i) for i in dataTrain]
ytrain = [i['hours'] for i in dataTrain]

Xtest = [feat1(i) for i in dataTest]
ytest = [i['hours'] for i in dataTest]

mod2 = LinearRegression()
mod2.fit(Xtrain, ytrain)
yhat2 = mod2.predict(Xtest)
mse2 = MSE(ytest, yhat2)

for i in range(len(yhat2)):
    if yhat2[i] > ytest[i]:
        over += 1
    else:
        under += 1

over, under

answers['Q2'] = [mse2, under, over]

assertFloatList(answers['Q2'], 3)

### Question 3



y2 = y[:]
y2.sort()
perc90 = y2[int(len(y2)*0.9)] # 90th percentile

X3a = [feat1(i) for i in dataTrain if i['hours'] <= perc90]
y3a = [i['hours'] for i in dataTrain if i['hours'] <= perc90]

mod3a = linear_model.LinearRegression()
mod3a.fit(X3a,y3a)
yhat3a = mod3a.predict(Xtest)

X3b = [feat1(i) for i in dataTrain]
y3b = [i['hours_transformed'] for i in dataTrain]

mod3b = linear_model.LinearRegression()
mod3b.fit(X3b,y3b)
yhat3b = mod3b.predict(Xtest)
yhat3b = np.array([2**i - 1 for i in yhat3b])

theta0 = mod2.coef_[0]

med_hours = np.median(np.array(y))
med_len = np.median(np.array(X)[:, 1])

theta1 = (med_hours-theta0)/med_len

yhat3c = [theta0 + theta1*i[1] for i in Xtest]
# yhat3c

under3a = 0
over3a = 0

under3b = 0
over3b = 0

under3c = 0
over3c = 0

for i in range(len(yhat3a)):
    if yhat3a[i] > ytest[i]:
        over3a += 1
    else:
        under3a += 1
for i in range(len(yhat3b)):
    if yhat3b[i] > ytest[i]:
        over3b += 1
    else:
        under3b += 1
for i in range(len(yhat3c)):
    if yhat3c[i] > ytest[i]:
        over3c += 1
    else:
        under3c += 1

# etc. for 3b and 3c
under3a, over3a, under3b, over3b, under3c, over3c



answers['Q3'] = [under3a, over3a, under3b, over3b, under3c, over3c]

assertFloatList(answers['Q3'], 6)

### Question 4

ytrain  = [1 if i['hours'] > med_hours else 0 for i in dataTrain]
ytest = [1 if i['hours'] > med_hours else 0 for i in dataTest]

Xtrain = [feat1(i) for i in dataTrain]
Xtest = [feat1(i) for i in dataTest]

mod = linear_model.LogisticRegression(C = 1)
mod.fit(Xtrain,ytrain)
predictions = mod.predict(Xtest) # Binary vector of predictions
predictions

predictions = np.array(predictions)
ytest = np.array(ytest)
TP = ((predictions ==1) & (ytest ==1)).sum()
FP = ((predictions ==1) & (ytest ==0)).sum()
TN = ((predictions ==0) & (ytest ==0)).sum()
FN = ((predictions ==0) & (ytest ==1)).sum()
BER = 1 - 0.5*(TP / (TP + FN) + TN / (TN + FP))

TP, FP, TN, FN, BER

answers['Q4'] = [TP, TN, FP, FN, BER]

assertFloatList(answers['Q4'], 5)

### Question 5

answers['Q5'] = [FP, FN]

assertFloatList(answers['Q5'], 2)

### Question 6

def BER(predictions, y):
  predictions = np.array(predictions)
  y = np.array(y)
  TP = ((predictions ==1) & (y ==1)).sum()
  FP = ((predictions ==1) & (y ==0)).sum()
  TN = ((predictions ==0) & (y ==0)).sum()
  FN = ((predictions ==0) & (y ==1)).sum()
  return 1 - 0.5*(TP / (TP + FN) + TN / (TN + FP))

Xtrain2014 = [feat1(i) for i in dataTrain if int(i['date'][:4]) <= 2014]
ytrain2014 = [i['hours'] for i in dataTrain if int(i['date'][:4]) <= 2014]
ytrain2014 = [1 if i > med_hours else 0 for i in ytrain2014]
Xtest2014 = [feat1(i) for i in dataTest if int(i['date'][:4]) <= 2014]
ytest2014 = [i['hours'] for i in dataTest if int(i['date'][:4]) <= 2014]
ytest2014 = [1 if i > med_hours else 0 for i in ytest2014]
ytest

mod6a = linear_model.LogisticRegression(C = 1)
mod6a.fit(Xtrain2014,ytrain2014)
predictions6a = mod6a.predict(Xtest2014)

BER_A = BER(predictions6a, ytest2014)


Xtrain2015 = [feat1(i) for i in dataTrain if int(i['date'][:4]) >= 2015]
ytrain2015 = [i['hours'] for i in dataTrain if int(i['date'][:4]) >= 2015]
ytrain2015 = [1 if i > med_hours else 0 for i in ytrain2015]
Xtest2015 = [feat1(i) for i in dataTest if int(i['date'][:4]) >= 2015]
ytest2015 = [i['hours'] for i in dataTest if int(i['date'][:4]) >= 2015]
ytest2015 = [1 if i > med_hours else 0 for i in ytest2015]

mod6b = linear_model.LogisticRegression(C = 1)
mod6b.fit(Xtrain2015,ytrain2015)
predictions6b = mod6b.predict(Xtest2015)

BER_B = BER(predictions6b, ytest2015)

mod6c = linear_model.LogisticRegression(C = 1)
mod6c.fit(Xtrain2014, ytrain2014)
predictions6c = mod6c.predict(Xtest2015)

BER_C = BER(predictions6c, ytest2015)

mod6d = linear_model.LogisticRegression(C = 1)
mod6d.fit(Xtrain2015, ytrain2015)
predictions6d = mod6d.predict(Xtest2014)


BER_D = BER(predictions6d, ytest2014)

BER_A, BER_B, BER_C, BER_D



answers['Q6'] = [BER_A, BER_B, BER_C, BER_D]

assertFloatList(answers['Q6'], 4)

### Question 7
dataTrain[0]

usersPerItem = defaultdict(set) # Maps an item to the users who rated it
itemsPerUser = defaultdict(set) # Maps a user to the items that they rated
reviewsPerUser = defaultdict(list)
reviewsPerItem = defaultdict(list)
dates = dict()

for d in dataTrain:
    user = d['userID']
    item = d['gameID']
    review = d['text']
    usersPerItem[item].add(user)
    itemsPerUser[user].add(item)
    reviewsPerUser[user].append(d)
    reviewsPerItem[item].append(d)
    dates[(user, item)] = d['date']

dates



def Jaccard(s1, s2):
  numer = len(s1.intersection(s2))
  denom = len(s1.union(s2))
  if denom == 0:
      return 0
  return numer / denom

def mostSimilar(i, N):
  similarities = []
  items = itemsPerUser[i]
  for i2 in itemsPerUser:
      if i2 == i: continue
      sim = Jaccard(items, itemsPerUser[i2])
      #sim = Pearson(i, i2) # Could use alternate similarity metrics straightforwardly
      similarities.append((sim,i2))
  similarities.sort(reverse=True)
  return similarities[:N]

sims = mostSimilar(dataTrain[0]['userID'], 10)
first = sims[0][0]
tenth = sims[9][0]

first, tenth

answers['Q7'] = [first, tenth]

assertFloatList(answers['Q7'], 2)

### Question 8

mean_hours_trans = np.mean([i['hours_transformed'] for i in dataTrain])
mean_hours_trans

def predictHoursi(user,item):
    hours = []
    similarities = []

    for d in reviewsPerUser[user]:
        i2 = d['gameID']
        if i2 == item: continue
        hours.append(d['hours_transformed'])
        similarities.append(Jaccard(usersPerItem[item],usersPerItem[i2]))
    if (sum(similarities) > 0):
        weightedRatings = [(x*y) for x,y in zip(hours,similarities)]
        return sum(weightedRatings) / sum(similarities)
    else:
        # User hasn't rated any similar items
        return mean_hours_trans

def predictHoursu(user,item):
    hours = []
    similarities = []
    for d in reviewsPerItem[item]:
        i2 = d['userID']
        if i2 == user: continue
        hours.append(d['hours_transformed'])
        similarities.append(Jaccard(itemsPerUser[user],itemsPerUser[d['userID']]))
    if (sum(similarities) > 0):
        weightedRatings = [(x*y) for x,y in zip(hours,similarities)]
        return sum(weightedRatings) / sum(similarities)
    else:
        # User hasn't rated any similar items
        return mean_hours_trans

def MSE(predictions, labels):
    differences = [(x-y)**2 for x,y in zip(predictions,labels)]
    return sum(differences) / len(differences)

yhatu = [predictHoursu(d['userID'], d['gameID']) for d in dataTest]
ytranstest = [i['hours_transformed'] for i in dataTest]
MSEU = MSE(yhatu, ytranstest)

yhati = [predictHoursi(d['userID'], d['gameID']) for d in dataTest]
MSEI = MSE(yhati, ytranstest)
MSEU, MSEI

answers['Q8'] = [MSEU, MSEI]

assertFloatList(answers['Q8'], 2)

### Question 9

def predictHoursuweight(user,item, date):
    hours = []
    similarities = []
    yrs = []


    for d in reviewsPerItem[item]:
        # print('hi')
        i2 = d['userID']
        if i2 == user: continue
        hours.append(d['hours_transformed'])
        similarities.append(Jaccard(itemsPerUser[user],itemsPerUser[d['userID']]))

        y2 = int(date[:4])
        y1 = int(d['date'][:4])
        yrs.append(np.exp(-np.abs(y2-y1)))
    if (sum(similarities) > 0):
        weightedRatings = [(x*y*z) for x,y,z, in zip(hours,similarities, yrs)]
        weightedsims = [(x*y) for x,y in zip(similarities, yrs)]
        return sum(weightedRatings) / sum(weightedsims)
    else:
        # User hasn't rated any similar items
        return mean_hours_trans


yhat9 = [predictHoursuweight(d['userID'], d['gameID'], d['date']) for d in dataTest]
MSE9 = MSE(yhat9, ytranstest)
MSE9

answers['Q9'] = MSE9

assertFloat(answers['Q9'])

if "float" in str(answers) or "int" in str(answers):
    print("it seems that some of your answers are not native python ints/floats;")
    print("the autograder will not be able to read your solution unless you convert them to ints/floats")

f = open("answers_midterm.txt", 'w')
f.write(str(answers) + '\n')
f.close()

answers

mean_hours_trans

