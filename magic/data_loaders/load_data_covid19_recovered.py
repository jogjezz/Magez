import pandas as pd
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    """
    Ingesting raw data from the COVID-19 Data Repository.
    """
    # URLs for the datasets
    recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv'
    
    # Load the datasets
    recovered_df = pd.read_csv(recovered_url)

    return recovered_df


@test
def test_output(df) -> None:
    """
    Test for the output of the raw data ingestion block.
    """
    assert df is not None, 'The output is undefined'
    assert not df.empty, 'The output dataframe is empty'
    assert 'Country/Region' in df.columns, 'The necessary columns are missing in the dataframe'
