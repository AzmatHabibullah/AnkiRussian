import pandas as pd
import requests
from tqdm import tqdm

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
        except Exception as e:
            print(f'Error with {row[1]}: {e}')
            words_df.iloc[i]['english'] = f'Error {e}'
    return words_df


def fetch_lingvo_data(n=1000):
    print("Fetching Lingvo data")
    words_df = pd.read_pickle("./clean_data/combined_table.pkl")
    words_df = words_df[['Rank', 'russian']][:n]
    words_df['lingvo_minicard_translation'] = ''
    # todo more new columns to come
    words_df = get_card_data(words_df)
    pd.to_pickle(words_df, f'words_with_lingvo_data_{len(words_df)}.pkl')
    print("Successfully fetched Lingvo data")
    fetch_lingvo_data()


if __name__ == "__main__":
    fetch_lingvo_data()
