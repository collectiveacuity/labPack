__author__ = 'rcj1492'
__created__ = '2016.03'

'''
http://angelhack.com/solve-these-developer-challenges-to-snag-free-tickets-to-our-series/
https://en.wikipedia.org/wiki/Braille
'''

class braille(object):

    def __init__(self):

        self.legend = {
            "a": [ 1, 0, 0, 0, 0, 0 ],
            "b": [ 1, 0, 1, 0, 0, 0 ],
            "c": [ 1, 1, 0, 0, 0, 0 ],
            "d": [ 1, 1, 0, 1, 0, 0 ],
            "e": [ 1, 0, 0, 1, 0, 0 ],
            "f": [ 1, 1, 1, 0, 0, 0 ],
            "g": [ 1, 1, 1, 1, 0, 0 ],
            "h": [ 1, 0, 1, 1, 0, 0 ],
            "i": [ 0, 1, 1, 0, 0, 0 ],
            "j": [ 0, 1, 1, 1, 0, 0 ],
            "k": [ 1, 0, 0, 0, 1, 0 ],
            "l": [ 1, 0, 1, 0, 1, 0 ],
            "m": [ 1, 1, 0, 0, 1, 0 ],
            "n": [ 1, 1, 0, 1, 1, 0 ],
            "o": [ 1, 0, 0, 1, 1, 0 ],
            "p": [ 1, 1, 1, 0, 1, 0 ],
            "q": [ 1, 1, 1, 1, 1, 0 ],
            "r": [ 1, 0, 1, 1, 1, 0 ],
            "s": [ 0, 1, 1, 0, 1, 0 ],
            "t": [ 0, 1, 1, 1, 1, 0 ],
            "u": [ 1, 0, 0, 0, 1, 1 ],
            "v": [ 1, 0, 1, 0, 1, 1 ],
            "w": [ 0, 1, 1, 1, 0, 1 ],
            "x": [ 1, 1, 0, 0, 1, 1 ],
            "y": [ 1, 1, 0, 1, 1, 1 ],
            "z": [ 1, 0, 0, 1, 1, 1 ]
        }

        self.binary = {}
        for key, value in self.legend.items():
            binary_pattern = ''
            for binary in value:
                binary_pattern += str(binary)
            self.binary[binary_pattern] = key

    def translate(self, braille_list):

        text_string = ''
        for item in braille_list:
            if item in self.binary.keys():
                text_string += self.binary[item]

        return text_string

    def transcribe(self, angelhack_sample):

    # prepare sample and determine number of characters
        binary_sample = angelhack_sample.replace('O','1').replace('.','0')
        collapsed_sample = binary_sample.replace(' ','')
        total_char = int(len(collapsed_sample) / 6)

    # transform into list of braille characters
        braille_list = []
        for i in range(0, total_char * 2, 2):
            braille_character = ''
            for j in range(3):
                k = i + (j * total_char * 2)
                braille_character += collapsed_sample[k]
                k += 1
                braille_character += collapsed_sample[k]
            braille_list.append(braille_character)

        return braille_list

sample = 'O. O. O. O. O. .O O. O. O. OO OO .O O. O. .O OO .O OO O. .O .. .. O. O. O. .O O. O. O. ..'
challenge = '.O O. .O OO O. O. .O OO O. OO O. .O O. .O O. .O O. .. .. OO OO .. .. .. OO OO .O OO O. O. O. O. .. O. O. O. OO .. .. .O O. .O'

bT = braille()
braille_list = bT.transcribe(challenge)
print(braille_list)
print(bT.translate(braille_list))

