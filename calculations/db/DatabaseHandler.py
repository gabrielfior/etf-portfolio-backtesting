
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from .models import Assets, Base
import pdb
from contextlib import contextmanager


@contextmanager
def session_scope(engine):
    """Provide a transactional scope around a series of operations."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        print ('commit now')
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class DatabaseHandler:
    def __init__(self, create_tables = False) -> None:
        # define DB
        #self.engine = create_engine('sqlite:///:memory:', echo=True)

        self.engine = create_engine('sqlite:///C:\\Users\\d91421\\code\\finance_predictions\\calculations\\db\\school.db', echo=True)
        self.tablename = Assets.__tablename__
        self.created_tables = False

        if create_tables:
            self.__create_all()
    
    def __create_all(self):
        Base.metadata.create_all(self.engine)
        self.created_tables = True

    def get_quotation(self,yahoo_ticker: str):
                
        with session_scope(self.engine) as session:
            users = session.query(Assets).filter_by(**{Assets.yahoo_ticker.name:yahoo_ticker}).all()
        return users
        #return pd.read_sql_query(
        #    f'''select * 
        #    from {self.tablename}
        #    where {Assets.yahoo_ticker.name} = "{yahoo_ticker}"''',
        #    self.engine,
        #    parse_dates=[Assets.date.name])


    def store_quotation(self, yahoo_ticker, df: pd.DataFrame) -> None:
        records = df.to_dict('records')

        records_db = Assets.from_yf(yahoo_ticker,[i for i in records])

        with session_scope(self.engine) as session:
            session.add_all(records_db)