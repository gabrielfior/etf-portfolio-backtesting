from .db.DatabaseHandler import DatabaseHandler
from typing import List
import yfinance as yf

class DataQuerier:
    def __init__(self):
        self.db_handler = DatabaseHandler(create_tables=True)

    def fetch_and_save(self, tickers: List[str],start:str=None,end:str=None,group_by:str='ticker',interval:str='1d',replace_local:bool=False):

        if group_by not in ['ticker','column']:
            raise TypeError('Must be either column or ticket')

        data = yf.download(tickers, start, end, group_by=group_by,
        interval=interval)
        
        # store locally for each ticker in sqlite DB
        for yahoo_ticker in tickers:
            df = data[yahoo_ticker]
            df.reset_index(inplace=True)
            self.db_handler.store_quotation(yahoo_ticker,df)

