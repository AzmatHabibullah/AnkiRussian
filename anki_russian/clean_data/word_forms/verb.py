from word import Word

class Verb(Word):

    def __init__(self, russian, english, aspect, transitional, prefix, example_sentences, **kwargs):
        super().__init__(russian=russian, english=english, example_sentences=example_sentences, part_of_speech='verb')
        self.aspect = aspect
        self.transitional = transitional
        self.prefix = prefix

        # I, me, we, you (pl), they
        self.past = kwargs.get('past', None)
        self.present = kwargs.get('present', None)
        self.future = kwargs.get('future', None)

