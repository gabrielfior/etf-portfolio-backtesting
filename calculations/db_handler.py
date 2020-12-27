import backtrader as bt

class DbHandler:

    def get_data_feed_by_name(self, data_feed_name, start, end):
        return bt.feeds.YahooFinanceData(dataname=data_feed_name,period='d', fromdate=start, todate=end)
