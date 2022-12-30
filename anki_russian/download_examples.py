from clean_database import get_using_api, RU_DICT, EN_DICT
import json

examples = {
    'noun': 'брат',
    'verb': 'брать',
    'adjective': 'умный',
    'numeral': 'первый',
    'adverb': 'тоже',
    'other': 'надо'
}

for key, value in examples.items():
    for request in ['fullcard', 'minicard', 'word_forms']:
        json_example = get_using_api(value, request, source_dict=RU_DICT, target_dict=EN_DICT, lang=RU_DICT)
        with open(f'./examples/{request}_{key}_{value}.json', 'w') as file:
            try:
                json.dump(json_example, file, indent=4)
            except:
                raise Exception(f"Some error occurred with {request} for {key} {value}")
