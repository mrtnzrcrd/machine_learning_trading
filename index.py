import requests
import pandas as pd
from pandas.io.json import json_normalize
import time
import datetime
import matplotlib.pyplot as plt

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window=window)

def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band

def plot_data(df, title="Stock prices"):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def getChartData(datefrom, dateto, currency_pair, period):
    from_int = repr(int(time.mktime(datetime.datetime.strptime(datefrom, "%Y-%m-%d").timetuple())))
    to_int = repr(int(time.mktime(datetime.datetime.strptime(dateto, "%Y-%m-%d").timetuple())))
    url = 'https://poloniex.com/public?command=returnChartData&currencyPair=' + currency_pair + '&start='+from_int+'&end='+to_int+'&period=' + period
    print(url)
    resp = requests.get(url)
    return json_normalize(resp.json())

def test_run():
    currency_pair = 'BTC_ETH'
    # 300, 900, 1800, 7200, 14400, and 86400
    period = '86400'
    date_from = '2017-01-01'
    date_to = '2017-06-04'

    dates = pd.date_range(date_from, date_to, freq=period+'s')
    df = pd.DataFrame(index=dates)
    df_temp = getChartData(date_from, date_to, currency_pair, period)

    df_temp['date'] = df_temp['date'].apply(lambda x:  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(x))))

    df_temp = df_temp.set_index(['date'])

    df = df.join(df_temp)

    #  A
    # df['close'] = df['close'].mean()
    # df = df / df.ix[0]
    # plot_data(df['close'])

    #  Compute Bollinger Bands
    # 1. Compute rolling mean
    rm_close = get_rolling_mean(df['close'], window=20)

    # 2. Compute rolling standard deviation
    rstd_close = get_rolling_std(df['close'], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_close, rstd_close)

    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df['close'].plot(title="Bollinger Bands", label='close')
    rm_close.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Close")
    ax.legend(loc='upper left')
    plt.show()


if __name__ == "__main__":
    test_run()