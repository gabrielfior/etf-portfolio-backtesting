import os
from calculations.db.DatabaseHandler import DatabaseHandler
from calculations.DataQuerier import DataQuerier
import pytest
import pandas as pd
import pathlib

@pytest.fixture(scope="module")
def init_db_handler() -> DatabaseHandler:
    return DatabaseHandler(create_tables=False)

@pytest.fixture(scope="module")
def test_historic_data() -> pd.DataFrame:
    curr_dir = os.path.dirname(__file__)
    return pd.read_pickle(pathlib.Path(curr_dir).joinpath('spy2.pickle'))

@pytest.fixture(scope="module")
def data_querier() -> DataQuerier:
    return DataQuerier()