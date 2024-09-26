import yfinance as yf
import datetime as datetime
import pytz

class Yahoo:
    def __init__(self):
        None

    def get_history(self, ticker, start_date: str = None, end_date: str = None, data_interval: int = 1, period: int = 1):
        """
        Get candles of one market.
        Args:
            start_time (str): start of data interval ['dd/mm/yyyy']
            end_time (str): end of data interval ['dd/mm/yyyy']
            data_interval (int): interval of data in minutes
            period (int): period of data in days

        """  
        ##  get data
        self.ticker = ticker
        self.data = yf.Ticker(ticker)

        ##  intervals and period conversion
        intervals = {1: '1m', 5: '5m', 15: '15m', 30: '30m', 90: '90m', 60: '1h', 1440: '1d', 7200: '5d', 10080: '1wk'}
        periods = {1: '1d', 5: '5d', 30: '1mo', 90: '3mo', 60: '2mo', 365: '1y', 730: '2y', 1825: '5y', 3650: '10y'}

        ##  check if data_interval and period are in the keys of intervals and periods
        if data_interval not in intervals.keys():
            raise Exception('data_interval not in intervals.keys()')
        if period not in periods.keys():
            raise Exception('period not in periods.keys()')
        
        if start_date != None and end_date != None:
            start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
            try:
                price_data = self.data.history(start=start_date, end=end_date, interval=intervals[data_interval], raise_errors=True, keepna=True)
                price_data.index = price_data.index.tz_convert(pytz.utc).rename('Date')
                return price_data
            except Exception as e:
                return e
        
        else: 
            try:
                price_data = self.data.history(interval=intervals[data_interval], period=periods[period], raise_errors=True, keepna=True)
                price_data.index = price_data.index.tz_convert(pytz.utc).rename('Date')
                return price_data
            except Exception as e:
                return e
    
    def get_info(self):
        """
        Get data of one market.

        """  
        try: 
            return self.data.info
        except Exception as e:
            return e