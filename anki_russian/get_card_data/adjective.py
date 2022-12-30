from utils import read_file
from translate import get_translation


def construct_card(fullcard, minicard):
    english = get_translation(fullcard, minicard)


if __name__ == "__main__":
    fullcard = read_file("example/minicard_adjective_умный.json")
    minicard = read_file("examples/fullcard_adjective_умный.json")
    word_forms = read_file("examples/word_forms_adjective_умный.json")
    construct_card(fullcard, minicard)