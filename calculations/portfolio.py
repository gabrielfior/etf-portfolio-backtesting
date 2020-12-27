from dataclasses import dataclass, field
from typing import List
from math import isclose
import datetime
import backtrader as bt

@dataclass
class EquityAllocation:
    data_name: str
    data_feed: bt.feed.FeedBase
    equity_allocation: float


@dataclass
class PortfolioHolder:
    allocations: List[EquityAllocation] = field(default_factory=list)
    
    def __post_init__(self):
        total_pct_allocation = sum([i.equity_allocation for i in self.allocations]) 
        if not isclose(total_pct_allocation, 1.0):
            raise ValueError('Sum of provided allocations {} != 1.0'.format(total_pct_allocation))

    def get_data_feeds(self):
        return [(alloc.data_name, alloc.data_feed) for alloc in self.allocations]

    def get_allocations(self):
        return [(alloc.data_name, alloc.equity_allocation) for alloc in self.allocations]

@dataclass
class CalculationContainer:
    datetime_index: List[datetime.datetime]
    value: List[float]