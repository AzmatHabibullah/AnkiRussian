from word import Word
from verb import Verb

verb = Verb(russian='есть', english='to eat', aspect='imperfective', transitional=False,
            prefix=None, example_sentences=['Я уже ел.'])


print(verb)  # repr
print(verb.part_of_speech)

verb  # str