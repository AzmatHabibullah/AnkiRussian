from wiktionaryparser import WiktionaryParser
import os
import pandas as pd
from tqdm import tqdm
from ..anki_utils import read_file


home_directory = os.getcwd()


def get_card_data(words, parser):
    for i, row in tqdm(enumerate(words.values)):
        print(row[1])
        try:
            wikidata = parser.fetch(row[1])
            long_definition = ''.join([f"{i + 1}: {x['text'][1]}; " for i, x in enumerate(wikidata[0]['definitions'][0:])])[:-2]
            short_definition = wikidata[0]['definitions'][0]['text'][1]
            words.iloc[i]['wiktionary_examples'] = ''.join([f"{i + 1}: {x}; " for i, x in enumerate(wikidata[0]['definitions'][0]['examples'])])[:-2]
            words.iloc[i][['wiktionary_short_definition', 'wiktionary_long_definition']] = [short_definition, long_definition]
        except Exception as e:
            print(f'Error with {row[1]}: {e}')
            words.iloc[i]['english'] = f'Error {e}'
        """
        for no, defn in enumerate(definitions):
            output[f'en_{no}_partOfSpeech'] = defn['partOfSpeech']
            output[f'en_{no}_defn'] = defn['text']
        """
    return words


def fetch_wiktionary_data(n=1000):
    print("Creating Wiktionary deck")
    parser = WiktionaryParser()
    parser.set_default_language("russian")
    words_df = pd.read_pickle("./clean_data/combined_table.pkl")
    words_df = words_df[['Rank', 'russian']][:n]
    words_df['wiktionary_short_definition'] = ''
    words_df['wiktionary_long_definition'] = ''
    words_df['wiktionary_examples'] = ''
    words_df = get_card_data(words_df, parser)
    pd.to_pickle(words_df, f'words_with_wiktionary_data_{len(words_df)}.pkl')
    print("Successfully created Wiktionary deck")


if __name__ == "__main__":
    fetch_wiktionary_data()




