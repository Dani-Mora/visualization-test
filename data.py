import pandas as pd

URL = 'https://analisi.transparenciacatalunya.cat/api/views/xuwf-dxjd/rows.csv'


def latest_data():
    df = pd.read_csv(URL)

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
