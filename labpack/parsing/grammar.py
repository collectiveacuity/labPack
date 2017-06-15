__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'


def join_words(word_list):

    text = ''
    for i in range(len(word_list)):
        if text:
            if i + 1 == len(word_list):
                text += ' and '
            else:
                text += ', '
        text += word_list[i]

    return text