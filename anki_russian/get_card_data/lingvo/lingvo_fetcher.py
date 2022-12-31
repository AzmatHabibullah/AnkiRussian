import pandas as pd


def get_card_data(words_df):
    # to come
    return words_df


def fetch_lingvo_data(n=1000):
    print("Fetching Lingvo data")
    words_df = pd.read_pickle("./clean_data/combined_table.pkl")
    words_df = words_df[['Rank', 'russian']][:n]
    words_df['lingvo_short_definition'] = ''
    # todo more new columns to come
    words_df = get_card_data(words_df)
    pd.to_pickle(words_df, f'words_with_lingvo_data_{len(words_df)}.pkl')
    print("Successfully fetched Lingvo data")
    fetch_lingvo_data()


if __name__ == "__main__":
    fetch_lingvo_data()
