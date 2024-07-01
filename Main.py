import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import tkinter as tk
import time

def data_loading(rate: str, dates: str, interval: str) -> pd.DataFrame:
    start_date, end_date = dates.split(' ')
    df = yf.download(rate, start = start_date, end = end_date, interval = interval).dropna()
    df.columns = ['open', 'high', 'low', 'close', 'adj close', 'volume']
    df.index.name = 'time'
    del df['adj close'], df['volume']
    df['var'] = df['close'].diff()
    return df
def sma(dataframe: pd.DataFrame, samples: int) -> pd.DataFrame:
    df['sma'] = df['close'].rolling(21).mean()
    return df['sma']
def ema(dataframe: pd.DataFrame, samples: int) -> pd.DataFrame:
    df['ema'] = df['close'].ewm(span = 200).mean()
    return df['ema']
def rsi(dataframe: pd.DataFrame, samples:int) -> pd.DataFrame:
    up, down =  df['var'].copy(), df['var'].copy()
    up[up < 0] = 0
    down[down > 0 ] = 0
    df['up'] = up
    df['down'] = down
    mean_up = up.rolling(samples).mean()
    mean_down = down.abs().rolling(samples).mean()
    rs = mean_up/mean_down
    df['rsi'] = 100 - (100/(1+rs))
    return rsi
def signal_gen(dataframe:pd.DataFrame) -> int:
    return
def draw( dataframe : pd.DataFrame, samples: int):
    plt.style.use('fivethirtyeight')
    fig, axes = plt.subplots(2, 1, figsize = (15, 10))
    axes[0].vlines(ymax = df['high'].iloc[-samples:], ymin = df['low'].iloc[-samples:],
                   x = df.index[-samples:], color = 'grey')
    axes[0].bar(height = df['up'].iloc[-samples:], x = df.index[-samples:],
                bottom = df['open'].iloc[-samples:], width = 0.05, color = 'g')
    axes[0].bar(height = df['down'].iloc[-samples:], x = df.index[-samples:],
                bottom = df['open'].iloc[-samples:], width = 0.05, color = 'r')
    axes[0].plot(df[['sma', 'ema']].iloc[-samples:])
    axes[0].legend(['_', 'Sma', 'Ema'])
    axes[1].plot(df['rsi'].iloc[-samples:], color = 'black')
    axes[1].axhline(y = 30, color = 'r', linewidth = 3, linestyle = 'dashed')
    axes[1].axhline(y = 70, color = 'r', linewidth = 3, linestyle = 'dashed')
    axes[1].legend(['Rsi'])

if __name__ == '__main__':
    df = data_loading('EURUSD=X', '2024-6-1 2024-7-1', '60m')
    sma(df, 21)
    ema(df, 200)
    rsi(df, 14)
    draw(df, 100)
    print('\nDone!')
