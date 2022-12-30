from word import Word

class Adjective(Word):

    def __init__(self, russian, english, type, example_sentences):
        super().__init__(russian=russian, english=english, example_sentences=example_sentences)
        self.type = type

        # todo edit