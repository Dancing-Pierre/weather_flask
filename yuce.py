import datetime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split


def shixu(testlen):

    df = pd.read_csv('weatherdata.csv')
    df = df[df['city']=='牡丹江']
    df = df[['aqi']]
    df.index=list(range(len(df)))
    print(df.shape)
    train = df[0:testlen]
    print(df)
    test = df[testlen:]
    # '''Holt-Winter 季节性平滑法'''
    from statsmodels.tsa.api import ExponentialSmoothing

    y_hat_avg = test.copy()
    for i in range(1,10):
        y_hat_avg.loc[df.shape[0]+i] = [0]
    print(train.shape)
    print(test.shape)
    # fit = Holt(np.asarray(train['y'])).fit(smoothing_level=0.1, smoothing_slope=0.5)
    fit=ExponentialSmoothing(np.asarray(train['aqi']), seasonal_periods=365,
                         trend='add', seasonal='add').fit()
    y_hat_avg['Holt_Winter'] = fit.forecast((len(test) + (10-1)))
    plt.figure(figsize=(16, 8))
    plt.plot(train['aqi'], label='Train')
    plt.plot(test['aqi'], label='Test')
    plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
    plt.plot(title='Holt-Winter 季节性平滑法')
    plt.legend(loc='best')
    plt.savefig('static/image/Holt.jpg')
    plt.show()
    holtlist = y_hat_avg['Holt_Winter']
    from math import sqrt
    y_hat_avg['Holt_Winter'].to_csv('Holt.csv')
    from sklearn.metrics import mean_squared_error
    rms = sqrt(mean_squared_error(test['aqi'], y_hat_avg['Holt_Winter'][:-9]))  #用RMSE检验准确率
    print(rms)

    return holtlist

if __name__ == '__main__':
    shixu(1600)