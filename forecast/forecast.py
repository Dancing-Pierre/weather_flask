import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge


def dataloader():
    X = pd.read_csv("./forecast/X.csv", index_col=0)
    Aqi = pd.read_csv("./forecast/aqi.csv", index_col=0)
    pm10 = pd.read_csv("./forecast/pm10.csv", index_col=0)
    pm25 = pd.read_csv("./forecast/pm2.5.csv", index_col=0)
    return X, Aqi, pm25, pm10


def pred_aqi(dataX):
    X, Aqi, pm25, pm10 = dataloader()
    X_train, X_test, Y_train, Y_test = train_test_split(X, Aqi, test_size=0.3)
    regr = Ridge(alpha=0.002, fit_intercept=True, random_state=0)
    regr.fit(X_train, Y_train)
    dataY = regr.predict(dataX)
    return dataY


def pred_pm25(dataX):
    X, Aqi, pm25, pm10 = dataloader()
    X_train, X_test, Y_train, Y_test = train_test_split(X, pm25, test_size=0.3)
    regr = Ridge(alpha=0.002, fit_intercept=True, random_state=0)
    regr.fit(X_train, Y_train)
    dataY = regr.predict(dataX)
    return dataY


def pred_pm10(dataX):
    X, Aqi, pm25, pm10 = dataloader()
    X_train, X_test, Y_train, Y_test = train_test_split(X, pm10, test_size=0.3)
    regr = Ridge(alpha=0.002, fit_intercept=True, random_state=0)
    regr.fit(X_train, Y_train)
    dataY = regr.predict(dataX)
    return dataY


def pred_sea(dataX):
    data = []
    for i in range(0, 3):
        date = ''
        # 返回aqi,pm2.5,pm10
        if dataX[0][0] == 0:
            city = '上海'
        else:
            city = '南京'
        if i == 0:
            date = '后面一天'
        elif i == 1:
            date = '后面两天'
        elif i == 2:
            date = '后面三天'
        aqi = pred_aqi(dataX)[0][0]
        aqi = '{:.2f}'.format(aqi)
        pm25 = pred_pm25(dataX)[0][0]
        pm25 = '{:.2f}'.format(pm25)
        pm10 = pred_pm10(dataX)[0][0]
        pm10 = '{:.2f}'.format(pm10)
        data_dict = {'city': city, 'date': date, 'aqi': aqi, 'pm2.5': pm25, 'pm10': pm10}
        data.append(data_dict)
        print(data_dict)
    return data

# dataX = [0, 2022, 2, 15]
# dataX = pd.DataFrame(dataX)
# dataX = dataX.T
# list = []
# for i in pred_sea(dataX):
#     a = '{:.2f}'.format(i)
#     list.append(a)
# print(list)
