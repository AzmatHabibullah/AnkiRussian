from anki_russian.db.db_creation import create_database
from anki_russian.clean_data.clean_database import clean_data
from get_card_data.wiktionary.cardDataFetcher import fetch_wiktionary_data
from create_deck.generate_anki_deck import generate_wiktionary_deck

LANGUAGE = 'russian'

if __name__ == "__main__":
    create_database()
    clean_data()
    fetch_wiktionary_data(n=25)
    generate_wiktionary_deck(n=25)
