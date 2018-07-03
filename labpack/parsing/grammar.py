__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'


def join_words(word_list, operator='conjuction', quotes=False):

    text = ''
    for i in range(len(word_list)):
        if text:
            if i + 1 == len(word_list):
                if operator == 'disjunction':
                    text += ' or '
                else:
                    text += ' and '
            else:
                text += ', '
        if quotes:
            text += '"'
        text += word_list[i]
        if quotes:
            text += '"'
            
    return text

def section_text(text_string, max_characters=500, continue_text='...'):

    if len(continue_text) + 2 > max_characters:
        raise ValueError('continue_text cannot be longer than max_characters - 2')
    
    from copy import deepcopy
    copy_string = deepcopy(text_string)
    
    string_sections = []
    
    while copy_string:
        if len(copy_string) > max_characters:
            text_index = max_characters - len(continue_text) - 1
            while text_index and copy_string[text_index] != ' ':
                text_index -= 1
            if text_index:
                text_end = text_index + 1
            else:
                text_index = max_characters - len(continue_text) - 1
                text_end = max_characters - len(continue_text)
            text_section = copy_string[0:text_end].strip() + continue_text
            string_sections.append(text_section)
            copy_string = copy_string[text_index:]
        else:
            string_sections.append(copy_string.strip())
            copy_string = ''
    
    return string_sections