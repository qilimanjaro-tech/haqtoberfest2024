import numpy as np
import pandas as pd
import yfinance


def fetch_log_returns(start,end):
    raw_data = yfinance.download(tickers = '^GSPC ^FTSE ^N225 ^GDAXI ^IBEX', 
                                start=start, end=end, interval = '1d', group_by = 'ticker',
                                auto_adjust = True)
    df_comp = pd.DataFrame(raw_data.copy())
    # pick data from the first day to the last one 
    df_comp = df_comp.iloc[1:]

    #add columns
    df_comp['sp500'] = df_comp['^GSPC'].Close[:]
    df_comp['dax'] = df_comp['^GDAXI'].Close[:]
    df_comp['ftse'] = df_comp['^FTSE'].Close[:]
    df_comp['nikkei'] = df_comp['^N225'].Close[:]
    df_comp['ibex'] = df_comp['^IBEX'].Close[:]

    #remove columns
    del df_comp['^GSPC'], df_comp['^GDAXI'], df_comp['^FTSE'], df_comp['^N225'], df_comp['^IBEX']

    price_data_frame = df_comp.asfreq('b') # only keeping bussiness days as the stock market is closed on weekends
    price_data_frame = df_comp.ffill() #forward fill
    price_data_frame = price_data_frame[1:]
    
    log_return = np.log(price_data_frame/price_data_frame.shift(1))
    log_return.columns = [c[0] for c in log_return.columns]
    return log_return.dropna()

def string_to_int_list(s):
    return [int(char) for char in s]
