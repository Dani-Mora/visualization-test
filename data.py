import pandas as pd

from datetime import datetime

DATA_COL = 'TipusCasData'
DIAGNOSE_COL = 'TipusCasDescripcio'

POSITIVE_STR = 'Positiu'
NEGATIVE_STR = 'Sospitós'


def latest_data():
    df = pd.read_csv('rows.csv')
    df[DATA_COL] = df[DATA_COL].apply(
        lambda x: datetime.strptime(x, '%d/%m/%Y')
    )
    return df


def tests_per_abs(df: pd.DataFrame) -> pd.DataFrame:

    def extract_stats(df: pd.DataFrame) -> pd.Series:
        return pd.Series({
            'TotalTests': df['NumCasos'].sum(),
            'Positius': df[
                df[DIAGNOSE_COL] == POSITIVE_STR]['NumCasos'].sum(),
            'Negatius': df[
                df[DIAGNOSE_COL] == NEGATIVE_STR]['NumCasos'].sum()
        })

    return df \
        .groupby(['ABSCodi', 'ABSDescripcio']) \
        .apply(extract_stats) \
        .reset_index()


def daily_tests(df: pd.DataFrame) -> pd.DataFrame:
    return df \
        .groupby([DATA_COL])['NumCasos'] \
        .sum() \
        .reset_index(name='Tests') \
        .fillna(0)


def daily_positive_rates(df: pd.DataFrame) -> pd.DataFrame:

    def _get_positive_perc(df: pd.DataFrame) -> float:
        positives = df[df[DIAGNOSE_COL] == POSITIVE_STR]['NumCasos'].sum()
        return round(positives / df['NumCasos'].sum() * 100, 2)

    return df \
        .groupby([DATA_COL]) \
        .apply(_get_positive_perc) \
        .reset_index(name='Percentatge positious') \
        .fillna(0)
