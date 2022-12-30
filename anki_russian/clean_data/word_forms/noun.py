from word import Word

class Noun(Word):

    def __init__(self, russian, english, gender, animate):
        super().__init__(russian, english, 'noun')
        self.gender = gender
        self.animate = animate
