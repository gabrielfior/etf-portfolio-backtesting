from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from enum import Enum
Base = declarative_base()



class Yf_Schema(Enum):
     DATE = 'Date'
     OPEN = "Open"
     HIGH = "High"
     LOW = "Low"
     CLOSE = "Close"
     ADJ_CLOSE = "Adj Close"
     VOLUME = "Volume"

class Assets(Base):
     __tablename__ = 'assets'

     id = Column(Integer, primary_key=True,autoincrement=True)
     yahoo_ticker = Column(String)
     date = Column(DateTime)
     open_price = Column(Float)
     high_price = Column(Float)
     low_price = Column(Float)
     close_price = Column(Float)
     adj_close_price = Column(Float)
     volume = Column(Float)

     @staticmethod
     def from_yf(yahoo_ticker, df_records):
          return [Assets.from_single_dict(yahoo_ticker,i) for i in df_records]
     
     @staticmethod
     def from_single_dict(yahoo_ticker,record):
          return Assets(**{Assets.yahoo_ticker.name: yahoo_ticker,
          Assets.date.name: record[Yf_Schema.DATE.value],
     Assets.open_price.name: record[Yf_Schema.OPEN.value],
     Assets.high_price.name: record[Yf_Schema.HIGH.value],
     Assets.low_price.name: record[Yf_Schema.LOW.value],
     Assets.close_price.name: record[Yf_Schema.CLOSE.value],
     Assets.adj_close_price.name: record[Yf_Schema.ADJ_CLOSE.value],
     Assets.volume.name: record[Yf_Schema.VOLUME.value]
          })