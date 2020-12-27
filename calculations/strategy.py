import backtrader as bt
import numpy as np

class BuyAndHoldTarget(bt.Strategy):
    # ToDo - Add etf allocation to init method

    params = (
            ('monthly_cash',None),  # amount of cash to buy every month
            ('etf_allocation',None) # PortfolioHolder
        )

    def start(self):
        # Activate the fund mode and set the default value at 100
        self.broker.set_fundmode(fundmode=True, fundstartval=100.00)
        self.cash_start = self.broker.get_cash()
        self.val_start = 100.0

        # Add a timer which will be called on the 1st trading day of the month
        self.add_timer(
            bt.timer.SESSION_END,  # when it will be called
            monthdays=[1],  # called on the 1st day of the month
            monthcarry=True,  # called on the 2nd day if the 1st is holiday
        )

    def buy_fixed_cash_amount_dummy(self, target_value, data_name):
        data_feed = self.getdatabyname(name=data_name)
        #return self.buy(exectype=bt.Order.Market,size=size,data=data_feed)
        value = self.broker.getvalue(datas=[data_feed])
        comminfo = self.broker.getcommissioninfo(data_feed)
        price = data_feed.close[0]     
        size = self.getsize(comminfo,price, target_value)
        print ('buying size {} of data {}, target_value {}'.format(size,data_name,target_value))
        return self.buy(data=data_feed, size=size, price=price)

    def getsize(self, comminfo, price, cash):
        if not comminfo._stocklike:
            return np.float(comminfo.p.leverage * (cash / comminfo.get_margin(price)))
        return np.float(1 * (cash / price))
        
    def notify_timer(self, timer, when, *args, **kwargs):
        # Add the influx of monthly cash to the broker
        self.broker.add_cash(self.p.monthly_cash)
        
        # buy available cash - we neglect the remaining value of cash, only invest the monthly amount
        #target_value = self.broker.getcash() + self.p.monthly_cash
        target_value = self.p.monthly_cash
        order_list = []
        
        for (data_name,percent_allocation) in self.p.etf_allocation.get_allocations():
            target = target_value*percent_allocation
            print ('buying {} from {} when {}, total target {}'.format(target, data_name, when, target_value))
            order = self.buy_fixed_cash_amount_dummy(target,data_name)
            if not order:
                print ('could not buy from {} when {}'.format(data_name, when))

    def stop(self):
        self.roi = (self.broker.get_value() / self.cash_start) - 1.0
        self.froi = self.broker.get_fundvalue() - self.val_start
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))
        print('Fund Value: {:.2f}%'.format(self.froi))
        print ('broker fund value {} broker val start {}'.format(self.broker.get_fundvalue(),self.val_start))