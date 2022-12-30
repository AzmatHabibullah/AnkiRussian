import json

import pandas as pd
import requests
import time

RU_DICT = 1049
EN_DICT = 1033
API_KEY = "NWQwODM4YTgtMDI3My00MDE3LTg1YjQtZGIxZjg1NjExZGI2OjA4MzE3MjE1YWU3ZjRmYzY4M2I3NTAxZjNhYWI5MDg1"
URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
URL_MINICARD = 'https://developers.lingvolive.com/api/v1/Minicard'
URL_FULLCARD = 'https://developers.lingvolive.com/api/v1/Translation'
URL_SOUND_FILE = 'https://developers.lingvolive.com/api/v1/Sound'
URL_WORD_FORMS = 'https://developers.lingvolive.com/api/v1/WordForms'


# todo generalise to get request and then chose request to specify return format
# todo check if can delete
def get_a_word_translation(key: str, url: str, source_dict=RU_DICT, target_dict=EN_DICT, return_full=False) -> str:
    headers_auth = {'Authorization': 'Basic ' + API_KEY}
    auth = requests.post(URL_AUTH, headers=headers_auth)
    if auth.status_code == 200:
        token = auth.text
        headers_translate = {
            'Authorization': 'Bearer ' + token
        }
        params = {
            'text': key,
            'srcLang': source_dict,
            'dstLang': target_dict
        }
        req = requests.get(
            url, headers=headers_translate, params=params)
        res = req.json()
        if return_full:
            return res
        try:
            value = res['Translation']['Translation']
            return value
        except TypeError:
            if res == 'Incoming request rate exceeded for 50000 chars per day pricing tier':
                return res
            else:
                return None
    else:
        print('Error!' + str(auth.status_code))


def clean_data():
    """
    Create word column and turn word type columns into booleans
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
