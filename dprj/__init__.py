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

        if current_letter == self.get_letters(self.position - 1, 1):
            self.position += 1
            return

        # The letter 'h' doesn't make any sense on its own, skip it
        if current_letter in 'aeouyh':
            self.position += 1
        elif current_letter == 'i':
            # Strip the 'll' if preceded by the letter 'i', except if it's the
            # first phoneme (eg. 'illumination')
            if self.position > 0 and self.get_letters(self.position + 1, 2) == 'll':
                self.position += 3
            else:
                self.position += 1
        elif current_letter == 'c':
            next_letters = self.get_letters(self.position + 1, 2)

            # 'accès', 'accident'
            if next_letters in ['ce', 'ci']:
                self.spell_and_move('ks', 2)
            # 'accord'
            elif self.get_next_letter() == 'c':
                self.spell_and_move('k', 2)
            # 'c' is pronounced 's' if followed by either 'i' or 'e'
            elif self.get_next_letter() in ['i', 'e']:
                self.spell_and_move('s', 1)
            elif self.get_next_letter() == 'h':
                # Some exceptions where 'ch' is pronounced 'k'
                ch_as_k_words = ['archange', 'charism', 'psycho', 'drachm']

                for word in ch_as_k_words:
                    if self.word.startswith(word):
                        self.spell_and_move('k', 2)
                        return

                # 'ch' followed by consonant = 'k' (eg. 'chrysanthème')
                if self.get_letters(self.position + 2, 1) not in 'aeiouy':
                    spelling = 'k'
                else:
                    spelling = 'x'
                self.spell_and_move(spelling, 2)
            else:
                self.spell_and_move('k', 1)
        elif current_letter == 'x':
            # Strip silent final 'x' (eg. 'barreaux')
            if not self.get_next_letter():
                self.position += 1
            elif self.get_next_letter() in 'aeiouyh':
                # 'x' is pronounced 'gz' if followed by a vowel and preceded by
                # an 'e' (eg. 'examen'), or 'ks' if preceded by another vowel
                # (eg. 'oxyde', 'axe')
                if self.get_letters(self.position - 1, 1) in 'e':
                    self.spell_and_move('gz', 1)
                else:
                    self.spell_and_move('ks', 1)
            else:
                self.spell_and_move(
                    'ks',
                    # 'x' followed by 'c' is 'ks' (eg. 'excès'), so skip the
                    # extra 'c' since we already have the 'ks' sound
                    1 if self.get_next_letter() != 'c' else 2
                )
        elif current_letter == 'p':
            # Easy one, 'ph' is always pronounced 'f'
            if self.get_letters(self.position + 1, 1) == 'h':
                self.spell_and_move('f', 2)
            else:
                self.spell_and_move('p', 1)
        elif current_letter == 't':
            # 'ti' is pronounced 's' in some cases (eg. 'action')
            if self.get_letters(self.position + 1, 2) in ['ie', 'ia', 'io']:
                self.spell_and_move('s', 3)
            # Final 't' is silent
            elif not self.get_next_letter() or self.get_next_letters(2) == 's':
                self.position += 1
            else:
                self.spell_and_move('t', 1)
        elif current_letter == 'g':
            # 'g' is pronounced 'j' if followed by 'i' or 'e' (eg. 'mage',
            # 'magicien')
            if self.get_letters(self.position + 1, 1) in 'ie':
                self.spell_and_move('j', 2)
            # 'g' followed by an 'n' is silent
            elif self.get_letters(self.position + 1, 1) != 'n':
                self.spell_and_move('g', 1)
            else:
                self.position += 1
        elif current_letter == 's':
            if self.get_letters(self.position + 1, 2) == 'ch':
                # 'schiz' (eg. 'schizophrène') is a special case where 'sch' is
                # pronounced 'sk', otherwise it's pronounced 'x' (eg.
                # 'schiste')
                if self.word.startswith('schiz'):
                    self.spell_and_move('sk', 3)
                else:
                    self.spell_and_move('x', 3)
            # If 's' is followed by 'ci' or 'ce', don't repeat the 's' sound
            # (eg. 'science'). Other vowels cause the 'c' to be pronounced (eg.
            # 'scaphandre')
            elif self.get_letters(self.position + 1, 2) in ['ci', 'ce']:
                self.spell_and_move('s', 2)
            # Final 's' is silent except for some words (is there any logic in
            # this?)
            elif not self.get_next_letter() and self.word not in ['oasis', 'anis', 'anus']:
                self.position += 1
            else:
                self.spell_and_move('s', 1)
        elif current_letter == 'l':
            # Final 'l' is silent if preceded by 'ei' (eg. 'oeil')
            if not self.get_next_letter() and self.get_letters(self.position - 2, 2) == 'ei':
                self.position += 1
            else:
                self.spell_and_move('l', 1)
        elif current_letter == 'f':
            # Final 'f' is silent if preceded by a consonant (eg. 'nerf').
            # Special case: 'clef'
            if ((not self.get_next_letter() or self.get_next_letters(2) == 's')
                    and ((self.get_letters(self.position - 1, 1) not in 'aeiouy')
                    or (self.word.startswith('clef')))):
                self.position += 1
            else:
                self.spell_and_move('f', 1)
        elif current_letter == 'd':
            # Final 'd' is silent (eg. 'accord')
            if not self.get_next_letter() or self.get_next_letters(2) == 's':
                self.position += 1
            else:
                self.spell_and_move('d', 1)
        else:
            self.spell_and_move(current_letter, 1)

    def get_next_letter(self):
        return self.get_next_letters(1)

    def get_next_letters(self, length):
        return self.get_letters(self.position + 1, length)

    def get_letters(self, position, length=1):
        return ''.join(self.word[position:position + length])

    def spell_and_move(self, sound, move):
        self.spelling += sound
        self.position += move


def say(word):
    w = Speller(word)
    w.spell()

    return w.spelling
