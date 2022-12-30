from word import Word

class Numeral(Word):

    def __init__(self, russian, english, type, example_sentences):
        super().__init__(russian=russian, english=english, example_sentences=example_sentences)
        self.type = type

        # todo edit - perhaps solve this case first as easiest

        # todo no.1 - download all examples of noun, verb, adjective, numeral,
        #  other so can work on this while code is running