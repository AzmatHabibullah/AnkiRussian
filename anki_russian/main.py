from db_creation import create_database
from clean_database import clean_data
from get_card_data.wiktionary.cardDataFetcher import createWiktionaryDeck
from create_deck.generate_anki_deck import generateWiktionaryDeck

LANGUAGE = 'russian'

if __name__ == "__main__":
    create_database()
    clean_data()
    createWiktionaryDeck()
    generateWiktionaryDeck()
