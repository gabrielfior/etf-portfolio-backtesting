from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

Base = declarative_base()

class Assets(Base):
     __tablename__ = 'assets'

     id = Column(Integer, primary_key=True)
     yahoo_ticker = Column(String)
     date = Column(DateTime)
     open_price = Column(Float)
     high_price = Column(Float)
     low_price = Column(Float)
     close_price = Column(Float)
     adj_close_price = Column(Float)
     volume = Column(Float)
