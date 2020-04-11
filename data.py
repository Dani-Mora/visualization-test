import pandas as pd

from datetime import datetime

URL = 'https://analisi.transparenciacatalunya.cat/api/views/xuwf-dxjd/rows.csv'


def latest_data():
    df = pd.read_csv(URL)
    df['Data'] = df['Data'].apply(
        lambda x: datetime.strptime(x, '%d/%m/%Y')
    )
    return df


def tests_per_abs(df: pd.DataFrame) -> pd.DataFrame:

    def extract_stats(df: pd.DataFrame) -> pd.Series:
        return pd.Series({
            'TotalTests': df['NumCasos'].sum(),
            'Positius': df[df['ResultatCovidCodi'] == 1]['NumCasos'].sum(),
            'Negatius': df[df['ResultatCovidCodi'] == 0]['NumCasos'].sum()
        })

    return df \
        .groupby(['ABSCodi', 'ABSDescripcio']) \
        .apply(extract_stats) \
        .reset_index()


def daily_tests(df: pd.DataFrame) -> pd.DataFrame:
    return df \
        .groupby(['Data'])['Data'] \
        .count() \
        .reset_index(name='Tests') \
        .fillna(0)


def daily_positive_rates(df: pd.DataFrame) -> pd.DataFrame:

    def _get_positive_perc(df: pd.DataFrame) -> float:
        positives = df[df['ResultatCovidCodi'] == 1]['NumCasos'].sum()
        return round(positives / df['NumCasos'].sum() * 100, 2)

    return df \
        .groupby(['Data']) \
        .apply(_get_positive_perc) \
        .reset_index(name='Percentatge positious') \
        .fillna(0)
