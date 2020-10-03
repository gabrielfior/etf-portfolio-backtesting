from sqlalchemy import create_engine

class DatabaseHandler:
    def __init__(self) -> None:
        # define DB
        self.engine = create_engine('sqlite:///:memory:', echo=True)