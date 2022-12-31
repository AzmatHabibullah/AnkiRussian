from anki_russian.db.db_creation import create_database
from anki_russian.clean_data.clean_database import clean_data
from get_card_data.wiktionary.wiktionary_fetcher import fetch_wiktionary_data
from get_card_data.lingvo.lingvo_fetcher import fetch_lingvo_data
from create_deck.generate_anki_deck import generate_wiktionary_deck

LANGUAGE = 'russian'

if __name__ == "__main__":
    #create_database()
    #clean_data()
    #fetch_wiktionary_data(n=25)
    fetch_lingvo_data(n=25)
    #generate_wiktionary_deck(n=25)
