from calculations.db.DatabaseHandler import DatabaseHandler
import pandas as pd
import pytest

@pytest.mark.skip
def test_insert_read(init_db_handler: DatabaseHandler, test_historic_data: pd.DataFrame):
    assert len(test_historic_data) > 0
    
    init_db_handler.store_quotation('SPY',test_historic_data)

    # assert if data was inserted
    inserted_df = init_db_handler.get_quotation('SPY')
    assert len(inserted_df) > 0
