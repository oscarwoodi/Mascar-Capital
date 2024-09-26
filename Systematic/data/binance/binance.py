from binance.client import Client
import time
from datetime import datetime, timedelta
import pytz
import pandas as pd

class Binance:
    def __init__(self, binance_api_key: str = None, binance_api_secret: str = None):
        ## binance client for price data
        self.binance_client = Client(binance_api_key, binance_api_secret)

    def get_history(self, ticker, start_date: str = None, end_date: str = None, data_interval: int = 1, period: int = 1):
        """
        Get candles of one market.
        Args:
            start_time (str): start of data interval ['dd/mm/yyyy']
            end_time (str): end of data interval ['dd/mm/yyyy']
            data_interval (int): interval of data in minutes
            period (int): period of data in days

        """  
        intervals = {1: self.binance_client.KLINE_INTERVAL_1MINUTE, 5: self.binance_client.KLINE_INTERVAL_5MINUTE, 15: self.binance_client.KLINE_INTERVAL_15MINUTE, 30: self.binance_client.KLINE_INTERVAL_30MINUTE, 60: self.binance_client.KLINE_INTERVAL_1HOUR, 240: self.binance_client.KLINE_INTERVAL_4HOUR, 1440: self.binance_client.KLINE_INTERVAL_1DAY}

        ##  check if data_interval and period are in the keys of intervals and periods
        if data_interval not in intervals.keys():
            raise Exception('data_interval not in intervals.keys()')
        
        try: 
            if start_date != None and end_date != None:
                start_date = datetime.strptime(start_date, '%d/%m/%Y').timestamp() * 1000
                end_date = datetime.strptime(end_date, '%d/%m/%Y').timestamp() * 1000
                limit = int((end_date - start_date) / (data_interval * 60 * 1000))

                try:
                    price_data = self.binance_client.futures_klines(symbol=ticker+'USDT', limit=limit, interval=intervals[data_interval])
                except Exception as e:
                    return e
                
            else: 
                try:
                    price_data = self.binance_client.futures_klines(symbol=ticker+'USDT', interval=intervals[data_interval], limit=int((period*24*60)/data_interval))
                except Exception as e:
                    return e
                
            ## Format data
            df = pd.DataFrame(price_data, columns=['open_timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_timestamp', 'quote_asset_vol', 'no_trades', 'taker_buy_base_asset_vol', 'taker_buy_quote_asset_vol', 'ignore'])
            df = df.rename(columns={'close_timestamp':'date', 'open':'Open', 'close':'Close', 'low':'Low', 'high':'High', 'volume':'Volume'})

            ## Truncate data
            df.drop(['open_timestamp', 'quote_asset_vol', 'no_trades', 'taker_buy_base_asset_vol', 'taker_buy_quote_asset_vol', 'ignore'], axis=1, inplace=True)
            df['Datetime'] = df['date'].map(lambda x: (int((float(x))/1000)+1))
            df = df[~(df['Datetime'] > time.time())]  ##  remove candle if it is in the future

            df['Datetime'] = df['Datetime'].map(lambda x: datetime.strptime(str(datetime.fromtimestamp(x)), '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc))
            df = df.set_index('Datetime').sort_index()

            df = df.astype(float)

            return df
        except Exception as e:
            return e