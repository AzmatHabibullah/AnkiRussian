import pandas as pd
import requests
from tqdm import tqdm
import json

RU_DICT = 1049
EN_DICT = 1033
API_KEY = "NWQwODM4YTgtMDI3My00MDE3LTg1YjQtZGIxZjg1NjExZGI2OjA4MzE3MjE1YWU3ZjRmYzY4M2I3NTAxZjNhYWI5MDg1"
URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
URL_MINICARD = 'https://developers.lingvolive.com/api/v1/Minicard'
URL_FULLCARD = 'https://developers.lingvolive.com/api/v1/Translation'
URL_SOUND_FILE = 'https://developers.lingvolive.com/api/v1/Sound'
URL_WORD_FORMS = 'https://developers.lingvolive.com/api/v1/WordForms'


def get_from_lingvo_api(text: str, request: str, **kwargs):
    """
    Get response from api for given request and text
    :param text: text to search
    :param request: one of 'minicard', 'fullcard', 'sound', 'word_forms'
    :param kwargs: 'source_dict', 'target_dict', 'is_case_sensitive', 'lang'
    :return: json if successful, status code if not
    """
    params = {
        'text': text,
    }
    if request == 'minicard':
        url = URL_MINICARD
        params['srcLang'] = kwargs['source_dict'],
        params['dstLang'] = kwargs['target_dict']
    elif request == 'fullcard':
        url = URL_FULLCARD
        params['srcLang'] = kwargs['source_dict'],
        params['dstLang'] = kwargs['target_dict']
        if not 'is_case_sensitive' in kwargs:
            kwargs['is_case_sensitive'] = False
        params['isCaseSensitive'] = kwargs['is_case_sensitive']
    elif request == 'sound':
        # todo
        url = URL_SOUND_FILE
    elif request == 'word_forms':
        url = URL_WORD_FORMS
        params['lang'] = kwargs['lang']
    else:
        raise KeyError("Request must be one of 'minicard', 'fullcard', 'sound', 'word_forms'")
    headers_auth = {'Authorization': 'Basic ' + API_KEY}
    auth = requests.post(URL_AUTH, headers=headers_auth)
    if auth.status_code == 200:
        token = auth.text
        headers_translate = {
            'Authorization': 'Bearer ' + token
        }
        req = requests.get(
            url, headers=headers_translate, params=params)
        return req.json()
    else:
        return auth.status_code


def get_card_data(words_df):
    for i, row in tqdm(enumerate(words_df.values)):
        print(row[1])
        try:
            lingvo_minicard = get_from_lingvo_api(text=row[1], request='minicard',
                                                  source_dict=RU_DICT, target_dict=EN_DICT)
            words_df.iloc[i]['lingvo_minicard_translation'] = lingvo_minicard['Translation']['Translation']

            lingvo_fullcard = get_from_lingvo_api(text=row[1], request='fullcard',
                                                  source_dict=RU_DICT, target_dict=EN_DICT)
            # todo: work through errors and determine how to extract data generally
            with open(f'examples/ordered/fullcard_{i}_{row[1]}', 'w') as file:
                try:
                    json.dump(lingvo_fullcard, file, indent=4)
                except:
                    raise Exception(f"Some error occurred with saving the file")
            audio_name = lingvo_fullcard[0]['Body'][0]['Markup'][0]['FileName']
            gender = lingvo_fullcard[0]['Body'][1]['Markup'][0]['Text']  # noun only
            words_df.iloc[i][['lingvo_gender', 'lingvo_audio_filename']] = gender, audio_name
            for defn_number, dict_entry in enumerate(lingvo_fullcard[0]['Body'][2]['Items']):
                node = dict_entry['Markup'][0]['Markup'][0]['Node']
                if 'IsItalics' in dict_entry['Markup'][0]['Markup'][0].keys():
                    italics = dict_entry['Markup'][0]['Markup'][0]['IsItalics']
                else:
                    italics = dict_entry['Markup'][0]['Markup'][0]['Markup'][0]['IsItalics']
                preamble = ''
                if node == 'Comment' or node == 'Abbrev' or italics:
                    preamble = dict_entry['Markup'][0]['Markup'][0]['Text']
                    defn = dict_entry['Markup'][0]['Markup'][1]['Text']
                elif node == 'Text':
                    defn = dict_entry['Markup'][0]['Markup'][0]['Text']
                else:
                    print(f"Node: {node}, italics: {italics} \t {dict_entry}")
                words_df.iloc[i][f'lingvo_defn_{defn_number+1}_preamble'] = preamble
                words_df.iloc[i][f'lingvo_defn_{defn_number+1}_defn'] = defn

        except Exception as e:
            print(f'Error with {row[1]}: {e}')
    return words_df


def fetch_lingvo_data(n=1000):
    print("Fetching Lingvo data")
    words_df = pd.read_pickle("./clean_data/combined_table.pkl")
    words_df = words_df[['Rank', 'russian']][:n]
    words_df['lingvo_minicard_translation'] = ''
    words_df['lingvo_gender'] = ''
    words_df['lingvo_audio_filename'] = ''
    for defn_number in range(10):
        for text_type in ['defn', 'preamble']:
            words_df[f'lingvo_defn_{defn_number+1}_{text_type}'] = ''
    words_df = get_card_data(words_df)
    pd.to_pickle(words_df, f'words_with_lingvo_data_{len(words_df)}.pkl')
    print("Successfully fetched Lingvo data")


if __name__ == "__main__":
    fetch_lingvo_data()
