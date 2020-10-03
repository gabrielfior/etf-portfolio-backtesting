import pdb
import pytest


def test_fetch_data(data_querier,init_db_handler):
    start = '2020-01-01'
    end = '2020-01-05'
    data_querier.fetch_and_save(['SPY','AAPL'],start=start,end=end)

    # see if data was inserted

    entries = init_db_handler.get_quotation('SPY')
    #pdb.set_trace()
    assert len(entries) > 0
