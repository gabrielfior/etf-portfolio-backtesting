from db_handler import DbHandler
from portfolio import EquityAllocation, PortfolioHolder
from engine import BacktraderEngine
from strategy import BuyAndHoldTarget
import datetime
import backtrader as bt
import matplotlib.pyplot as plt

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