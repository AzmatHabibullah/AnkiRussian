import pandas as pd


def clean_data():
    """
    Create overall word column and turn word type columns into booleans
    """
    print("Cleaning Wiktionary database")
    df = pd.read_pickle('./db/combined_table.pkl')
    df['russian'] = df.mask(df == '')[[x for x in df.columns if x != 'Rank']].fillna(method='bfill', axis=1).iloc[:, 0]
    for col in [c for c in df.columns if (c != 'Rank' and c != 'russian')]:
        df[col] = df[col] != ''
    df.to_pickle('./clean_data/combined_table.pkl')
    print("Successfully cleaned Wiktionary database")


if __name__ == "__main__":
    clean_data()
