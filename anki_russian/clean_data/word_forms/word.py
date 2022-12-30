class Word:

    def __init__(self, russian, english, example_sentences, part_of_speech='other'):
        self.russian = russian
        self.english = english
        self.example_sentences = example_sentences
        self.part_of_speech = part_of_speech


    def __str__(self):
        return f'{self.russian}: {self.english} ({self.part_of_speech})'


    def __repr__(self):
        return f'{self.russian}: {self.english} ({self.part_of_speech}). ' \
               f'Examples: {self.example_sentences}'