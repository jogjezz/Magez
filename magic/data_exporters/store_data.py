from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
import pandas as pd
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_exporter
def export_data_to_postgres( recovered_df: DataFrame, confirmed_df: DataFrame, deaths_df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'public'  # Specify the name of the schema to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # Print statements to verify the source of each dataframe
    # print("Data from load_data_confirmed:", confirmed_df.head())
    # print("Data from load_data_recovered:", recovered_df.head())
    # print("Data from load_data_death:", deaths_df.head())

    stg_confirmed_df = transform_data(confirmed_df)
    stg_recovered_df = transform_data(recovered_df)
    stg_deaths_df = transform_data(deaths_df)

    
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        # Export the DataFrame to PostgreSQL
        loader.export(
            stg_confirmed_df,
            schema_name,
            "covid19_confirmed",
            index=False,  # Specifies whether to include index in the exported table
            if_exists='replace',  # Specify resolution policy if the table name already exists
        )

        loader.export(
            stg_recovered_df,
            schema_name,
            "covid19_recovered",
            index=False,  # Specifies whether to include index in the exported table
            if_exists='replace',  # Specify resolution policy if the table name already exists
        )

        loader.export(
            stg_deaths_df,
            schema_name,
            "covid19_deaths",
            index=False,  # Specifies whether to include index in the exported table
            if_exists='replace',  # Specify resolution policy if the table name already exists
        )

    return stg_confirmed_df



def transform_data(df: DataFrame) -> DataFrame:
    # Transform the data to fit the table structure
    df_melted = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')
    df_melted['Date'] = pd.to_datetime(df_melted['Date']).dt.strftime('%Y-%m-%d')

    # Fill missing values to avoid dropping rows
    df_melted['Province/State'].fillna('None', inplace=True)

    df_pivoted = df_melted.pivot_table(index=['Province/State', 'Country/Region', 'Lat', 'Long'], columns='Date', values='Confirmed', fill_value=0).reset_index()
    df_pivoted.columns.name = None

    # Convert DataFrame to JSONB format
    df_pivoted['confirmed_cases'] = df_pivoted.loc[:, df_pivoted.columns.str.match(r'\d{4}-\d{2}-\d{2}')].apply(lambda row: row.to_dict(), axis=1)

    # Select necessary columns
    df_final = df_pivoted[['Province/State', 'Country/Region', 'Lat', 'Long', 'confirmed_cases']]

    # Rename columns to match table structure
    df_final.columns = ['province_state', 'country_region', 'lats', 'longs', 'cases']

    return df_final

@test
def test_output(df) -> None:
    """
    Test for the output of the data storage block.
    """
    assert df is not None, 'The output is undefined'
    assert not df.empty, 'The output dataframe is empty'
    assert 'cases' in df.columns, 'The necessary JSONB column is missing in the dataframe'
