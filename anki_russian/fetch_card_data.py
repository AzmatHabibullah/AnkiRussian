import time

import requests

RU_DICT = 1049
EN_DICT = 1033
API_KEY = "NWQwODM4YTgtMDI3My00MDE3LTg1YjQtZGIxZjg1NjExZGI2OjA4MzE3MjE1YWU3ZjRmYzY4M2I3NTAxZjNhYWI5MDg1"
URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
URL_MINICARD = 'https://developers.lingvolive.com/api/v1/Minicard'
URL_FULLCARD = 'https://developers.lingvolive.com/api/v1/Translation'
URL_SOUND_FILE = 'https://developers.lingvolive.com/api/v1/Sound'
URL_WORD_FORMS = 'https://developers.lingvolive.com/api/v1/WordForms'

def get_using_api(text: str, request: str, **kwargs):
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


def get_details(example):
    wav_file = example['Body']['Markuo']['FileName']
    translation = example['Body']['Items']['Markup']['Markup']['Text']


# todo check if can delete
def translation(word):
    time.sleep(2)
    mini_card = get_using_api(word, 'minicard', source_dict=RU_DICT, target_dict=EN_DICT)
    if type(mini_card) != dict:
        print(word + ":" + mini_card)
        return mini_card
    try:
        defn = mini_card['Translation']['Translation']
        print(word + ":" + defn)
        return defn
    except Exception as e:
        return f"error {e}"