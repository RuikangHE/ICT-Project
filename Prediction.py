# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 02:15:32 2020

@author: 2369158615@qq.com
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression

data = pd.read_excel("C:\\Users\\23691\\Desktop\\Wheels History.xlsx")
data = data[data[data.columns[0]] == "CM3306H"]
data = data.sort_values(by=data.columns[1], ascending=True, ignore_index=True)
data['Measure Date'] = pd.to_datetime(data['Measure Date'])
data['Measure Date']=data['Measure Date'].map(dt.datetime.toordinal)
print(data['L2-RIM/DIA'])

x_d = []
y = []
row = data.shape[0] #row count
d = data.loc[row - 1, "Measure Date"]
for x in range(1, row):
    # selecting specific row and column
    if(data.loc[x, "L2-RIM/DIA"] > 100):
        data.loc[x, "L2-RIM/DIA"] = round(0.0393701 * data.loc[x, "L2-RIM/DIA"], 1)
    if(data.loc[ x, "L2-RIM/DIA"] < data.loc[ x - 1, "L2-RIM/DIA"] and data.loc[ x, "L2-RIM/DIA"] < 100 and data.loc[ x-1, "L2-RIM/DIA"] < 100):
        date_format = '%Y-%m-%d %H:%M:%S'
        a = data.loc[x - 1, "Measure Date"]
        b = data.loc[x, "Measure Date"]
        delta = b - a
        c = data.loc[ x - 1, "L2-RIM/DIA"] - data.loc[ x, "L2-RIM/DIA"]
        x_d.append(delta)
        y.append(c)
date = pd.DataFrame(x_d, columns = ['Measure Date'])
dia = pd.DataFrame(y, columns = ['L2-RIM/DIA'])
print(date)
print(dia)

y_final = date
x_final = dia

x_train, x_test, y_train, y_test = train_test_split(x_final, y_final, test_size = 0.33, random_state = 0)
###normalized scaler (fit transform on train, fit only on test)
n_scaler = MinMaxScaler()
x_train = n_scaler.fit_transform(x_train.astype(np.float))
x_test= n_scaler.transform(x_test.astype(np.float))

###standard scaler (fit transform on train, fit only on test)
s_scaler = StandardScaler()
x_train = s_scaler.fit_transform(x_train.astype(np.float))
x_test= s_scaler.transform(x_test.astype(np.float))

lr = LinearRegression().fit(x_train, y_train)
y_train_pred = lr.predict(x_train)
y_test_pred = lr.predict(x_test)

print("lr.coef_: {}".format(lr.coef_))
print("lr.intercept_:{}".format(lr.intercept_))
print('lr train score %.3f, lr test score: %.3f' % (
    lr.score(x_train, y_train),
    lr.score(x_test, y_test)))
print(dt.datetime.fromordinal(lr.predict([[5]])[0] + d))
