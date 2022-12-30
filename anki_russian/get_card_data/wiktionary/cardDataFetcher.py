from wiktionaryparser import WiktionaryParser
import os
import json
import pandas as pd
from tqdm import tqdm

home_directory = os.getcwd()


def read_file(relative_dir):
    if ".txt" in relative_dir:
        with open(home_directory + relative_dir, 'r') as file:
            return file
    elif ".xlsx" in relative_dir or ".xls" in relative_dir:
        return pd.read_excel(home_directory + relative_dir)
    elif ".json" in relative_dir:
        with open(home_directory + relative_dir, 'r') as file:
            return json.load(file)
    elif ".pkl" in relative_dir:
        return pd.read_pickle(home_directory + relative_dir)
    else:
        with open(home_directory + relative_dir, 'r') as file:
            return file


def getCardData(words, parser):
    for i, row in tqdm(enumerate(words.values)):
        print(row[1])
        try:
            wikidata = parser.fetch(row[1])
            # todo: for definition in definitions, add to 'wiktionary_definition_x'
            long_definition = ''.join([f"{i + 1}: {x['text'][1]}; " for i, x in enumerate(wikidata[0]['definitions'][0:])])[:-2]
            short_definition = wikidata[0]['definitions'][0]['text'][1]
            words.iloc[i]['english_examples'] = ''.join([f"{i + 1}: {x}; " for i, x in enumerate(wikidata[0]['definitions'][0]['examples'])])[:-2]
            words.iloc[i][['english_short_definition', 'english_long_definition']] = [short_definition, long_definition]
        except Exception as e:
            print(f'Error with {row[1]}: {e}')
            words.iloc[i]['english'] = f'Error {e}'
        """
        for no, defn in enumerate(definitions):
            output[f'en_{no}_partOfSpeech'] = defn['partOfSpeech']
            output[f'en_{no}_defn'] = defn['text']
        """
    return words


def createWiktionaryDeck():
    print("Creating Wiktionary deck")
    parser = WiktionaryParser()
    parser.set_default_language("russian")
    words = read_file("/clean_data/combined_table.pkl")
    words = words[['Rank', 'russian']][:750]
    words['english_short_definition'] = ''
    words['english_long_definition'] = ''
    words['english_examples'] = ''
    words = getCardData(words, parser)
    pd.to_pickle(words, 'wiktionary_top10.pkl')
    print("Successfully created Wiktionary deck")


if __name__ == "__main__":
    createWiktionaryDeck()




