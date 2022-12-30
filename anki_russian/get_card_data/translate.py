def get_numeral_details(full_card, mini_card):
    russian = mini_card['Heading']
    english = mini_card['Translation']['Translation']
    sound_name = mini_card['Translation']['SoundName']

    check_lingvo(full_card[0])
    # todo get stress from "IsAccent"==True in "TitleMarkup"
    russian = full_card[0]['Title']
    sound_name = full_card[0]['Body'][0]['Markup'][0]['FileName']

    definitions = full_card[0]['Body'][2]['Markup']
    output = []
    for x in definitions[:2]:
        output.append([])


def check_lingvo(card):  # fullcard only
    assert card['Dictionary'] == 'LingvoUniversal (Ru-En)' or card['Dictionary'] == 'LingvoUniversal (En-Ru)'


def get_translation(full_card, mini_card):
    english = mini_card['Translation']['Translation']

    return english

