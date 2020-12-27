import datetime
from portfolio import PortfolioHolder, EquityAllocation
from dataclasses import dataclass
import backtrader as bt
import empyrical as ep
import pandas as pd
from backtrader.utils.py3 import iteritems
import pyfolio as pf
from db_handler import DbHandler

@dataclass
class BacktraderEngine:
    portfolio: PortfolioHolder
    strategy: bt.Strategy
    cerebro: bt.Cerebro
    strategy_args: dict

    def __post_init__(self):
        # Add a strategy
        self.cerebro.addstrategy(self.strategy, **self.strategy_args)
        self.cerebro.broker.set_cash(0.000001)
        self.cerebro.broker.set_fundmode(True)

        for data_name,data_feed in self.portfolio.get_data_feeds():
            self.cerebro.adddata(data_feed, name=data_name)


        # Observers
        self.cerebro.addobserver(bt.observers.TimeReturn, timeframe=bt.TimeFrame.Days)

        # Analyzers
        self.cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio', timeframe=bt.TimeFrame.Days)
        self.cerebro.addanalyzer(bt.analyzers.PositionsValue, headers=True, cash=True, _name='mypositions')
        self.cerebro.addanalyzer(bt.analyzers.TimeReturn,_name='timereturn')

    
    def get_returns(self):

        results = self.cerebro.run()

        strat = results[0]
        pyfoliozer = strat.analyzers.getbyname('pyfolio',)
        returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items() #<--positions only holds data for one symbol here

        p = strat.analyzers.getbyname('mypositions').get_analysis()
        mypositions = [[k] + v for k, v in iteritems(p)] #<-- Now positions will hold data for all symbols
        cols = mypositions.pop(0)  # headers are in the first entry
        mypositions = pd.DataFrame.from_records(mypositions, index=cols[0], columns=cols)
        mypositions.index = pd.DatetimeIndex(mypositions.index) 

        mypositions['total'] = mypositions.sum(axis=1)
        myreturns = mypositions['total'].pct_change()
        myreturns.index = pd.to_datetime(myreturns.index).tz_localize('US/Eastern')
        
        timereturn_analyzer = strat.analyzers.getbyname('timereturn')
        timereturn = timereturn_analyzer.get_analysis()

        timereturn_df = pd.DataFrame([(k,v) for k,v in timereturn.items()],columns=['date','return'])
        timereturn_df.set_index('date',inplace=True)

        a=pf.timeseries.extract_interesting_date_ranges(timereturn_df['return'])
        
        series =  (a[list(a.keys())[0]])
        return ep.cum_returns(series)

    def get_buy_and_hold_returns():
        # aa
        

        start=datetime.datetime(2020,1,1)
        end=datetime.datetime(2020,12,1)

        db_handler = DbHandler()
        data_vusa = db_handler.get_data_feed_by_name('VUSA.DE',start,end)
        data_stoxx = db_handler.get_data_feed_by_name('EXSA.DE',start,end)

        portfolio = PortfolioHolder([
            EquityAllocation('VUSA.DE',data_vusa, 0.5),
            EquityAllocation('EXSA.DE',data_stoxx, 0.5)
        ])

        strategy_args = {'monthly_cash':700, 'etf_allocation':portfolio}
        engine = BacktraderEngine(portfolio, BuyAndHoldTarget, bt.Cerebro(), strategy_args)
        print ('calling returns')
        returns = engine.get_returns()
        plt.figure()
        plt.plot(returns)
        plt.show()
                
