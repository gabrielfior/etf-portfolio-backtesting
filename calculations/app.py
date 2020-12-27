from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
from db_handler import DbHandler
from portfolio import EquityAllocation, PortfolioHolder
from engine import BacktraderEngine
from strategy import BuyAndHoldTarget
import datetime
import backtrader as bt
import matplotlib.pyplot as plt

app = FastAPI()

class AssetAllocation(BaseModel):
    yticker: str
    allocation: float

class CalculationRequest(BaseModel):
    start_date: datetime.datetime
    end_date: datetime.datetime
    equities: List[AssetAllocation]
    monthly_amount: float


@app.post("/run_calculation/")
async def create_item(calc_request: CalculationRequest):
    # do calculations
    db_handler = DbHandler()

    if calc_request.start_date.day == calc_request.end_date.day:
        raise HTTPException(status_code=400, detail="Start date and end date must be at least 1 day apart")

    if (calc_request.end_date - calc_request.start_date).days <= 0:
        raise HTTPException(status_code=400, detail="Start date and end date must be at least 1 day apart")

    list_equities = [EquityAllocation(
        equity.yticker,
        db_handler.get_data_feed_by_name(equity.yticker, calc_request.start_date, calc_request.end_date),
        equity.allocation) for equity in calc_request.equities]

    portfolio = PortfolioHolder(list_equities)

    strategy_args = {'monthly_cash': calc_request.monthly_amount, 'etf_allocation': portfolio}
    engine = BacktraderEngine(portfolio, BuyAndHoldTarget, bt.Cerebro(), strategy_args)
    returns = engine.get_returns()
    return returns