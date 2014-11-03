# -*- coding: utf-8 -*-
import re
import unicodedata


class Speller(object):
    def __init__(self, word):
        self.position = 0
        self.word = self.global_substitutions(word)
        self.spelling = u''

    def spell(self):
        done = False

        while True:
            if self.position >= len(self.word):
                break

            self.handle_letter()

        return self.spelling

    def global_substitutions(self, word):
        word = word.replace(u'ç', 's')
        word = word.replace('q', 'k')
        word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('ascii')

        return word

    def handle_letter(self):
        current_letter = self.word[self.position]

        # The letter 'h' doesn't make any sense on its own
        if current_letter in 'aeouyh':
            self.position += 1
        elif current_letter == 'i':
            if self.position > 0 and self.get_letters(self.position + 1, 2) == 'll':
                self.position += 3
            else:
                self.position += 1
        elif current_letter == 'c':
            next_letters = self.get_letters(self.position + 1, 2)

            if next_letters in ['ce', 'ci']:
                self.spelling += 'ks'
                self.position += 2
            elif self.get_next_letter() == 'c':
                self.spelling += 'k'
                self.position += 2
            elif self.get_next_letter() in ['i', 'e']:
                self.spelling += 's'
                self.position += 1
            # TODO plurals
            elif self.get_next_letter() == 'h':
                ch_as_k_words = ['archange', 'charism']

                for word in ch_as_k_words:
                    if self.word.startswith(word):
                        self.spelling += 'k'
                        self.position += 2
                        return

                # ch + consonant = k (eg. chrysanthème)
                if self.get_letters(self.position + 2, 1) not in 'aeiouy':
                    self.spelling += 'k'
                else:
                    self.spelling += 'x'
                self.position += 2
            else:
                self.spelling += 'k'
                self.position += 1
        elif current_letter == 'x':
            if not self.get_next_letter():
                self.position += 1
            elif self.get_next_letter() in 'aeiouy':
                if self.get_letters(self.position - 1, 1) == 'e':
                    self.spelling += 'gz'
                    self.position += 1
                else:
                    self.spelling += 'ks'
                    self.position += 1
            else:
                self.spelling += 'ks'
                self.position += 1 if self.get_next_letter() != 'c' else 2
        elif current_letter == 'p':
            if self.get_letters(self.position + 1, 1) == 'h':
                self.spelling += 'f'
                self.position += 2
            else:
                self.spelling += 'p'
                self.position += 1 if self.get_next_letter() != 'p' else 2
        elif current_letter == 't':
            if self.get_letters(self.position + 1, 2) in ['ie', 'ia', 'io']:
                self.spelling += 's'
                self.position += 3
            elif not self.get_next_letter():
                self.position += 1
            else:
                self.spelling += 't'
                self.position += 1 if self.get_next_letter() != 't' else 2
        elif current_letter == 'g':
            if self.get_letters(self.position + 1, 1) in ['i', 'e']:
                self.spelling += 'j'
                self.position += 2
            elif self.get_letters(self.position + 1, 1) != 'n':
                self.spelling += 'g'
                self.position += 1
            else:
                self.position += 1
        elif current_letter == 's':
            # schiste, schizophrène
            if self.get_letters(self.position + 1, 2) == 'ch':
                if self.word.startswith('schiz'):
                    self.spelling += 'sk'
                    self.position += 3
                else:
                    self.spelling += 'x'
                    self.position += 3
            # science
            elif self.get_letters(self.position + 1, 1) == 'c':
                self.spelling += 's'
                self.position += 2
            elif not self.get_next_letter() and self.word not in ['oasis', 'anis', 'anus']:
                self.position += 1
            else:
                self.spelling += 's'
                self.position += 1 if self.get_next_letter() != 's' else 2
        elif current_letter == 'l':
            if not self.get_next_letter() and self.get_letters(self.position - 2, 2) == 'ei':
                self.position += 1
            else:
                self.spelling += 'l'
                self.position += 1 if self.get_next_letter() != 'l' else 2
        # TODO plural
        elif current_letter == 'f':
            if not self.get_next_letter():
                self.position += 1
            else:
                self.spelling += 'f'
                self.position += 1 if self.get_next_letter() != 'f' else 2
        else:
            self.spelling += current_letter
            self.position += 1 if self.get_next_letter() != current_letter else 2


    def get_next_letter(self):
        return self.get_letters(self.position + 1, 1)

    def get_letters(self, position, length=1):
        return ''.join(self.word[position:position + length])


def say(word):
    w = Speller(word)
    w.spell()

    return w.spelling
