import genanki
import pandas as pd


def create_wiktionary_model():
    model = genanki.Model(
        model_id=1668450076,  # generated by model_id = random.randrange(1 << 30, 1 << 31), as per genanki docs
        name='Russian deck',
        fields=[
            {'name': 'Russian'},  # todo change to language
            {'name': 'English long defn'},  # todo add conjugation, declension
            {'name': 'English short defn'},
            {'name': 'English examples'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Russian}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{English short defn}}<br/><br/><b>'
                        'All definitions</b><br/>{{English long defn}}<br/><br/>'
                        '<b>Examples</b><br/>{{English examples}}'
            }
        ],
        css='.card {text-align: center}'
    )
    return model


def create_wiktionary_deck(wiktionary_model, wiktionary_notes):
    wiktionary_deck = genanki.Deck(
        deck_id=1239871986,  # generated by deck_id = random.randrange(1 << 30, 1 << 31), as per genanki docs
        name=f'Russian to English top {len(wiktionary_notes)}',
        description='Russian to English deck: top 5k words from Wiktionary'
    )
    return wiktionary_deck


def add_notes_to_deck(deck, model, notes):
    words_dict = notes.to_dict(orient='records')
    for row in words_dict:
        note = genanki.Note(
            model=model,
            fields=[row['russian'], row['english_long_definition'], row['english_short_definition'], row['english_examples']]
        )
        deck.add_note(note)
    print(deck.notes)


def read_frame(source):
    return pd.read_pickle(f'{source}.pkl')


def save_deck_to_disk(deck):
    genanki.Package(deck).write_to_file(deck.name + '.apkg')


def generate_wiktionary_deck():
    wiktionary_model = create_wiktionary_model()
    wiktionary_notes = read_frame('wiktionary_top10')
    wiktionary_deck = create_wiktionary_deck(wiktionary_model, wiktionary_notes)
    add_notes_to_deck(wiktionary_deck, wiktionary_model, wiktionary_notes)
    save_deck_to_disk(wiktionary_deck)


if __name__ == "__main__":
    generate_wiktionary_deck()