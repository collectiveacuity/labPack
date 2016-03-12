__author__ = 'rcj1492'
__created__ = '2016.03'

'''
interactions with unix shell
https://stackoverflow.com/questions/1494178/how-to-define-hash-tables-in-bash
'''

def parseSh(file_name):
    var_dict = {}
    end_line = compile('\\n$')
    comment_out = compile('#')
    space_char = compile('\\s')
    export_cmd = compile('^export\\s')
    with open(file_name) as f:
        for line in f:
            if not comment_out.match(line):
                if len(line.split('=')) == 2:
                    k, v = line.split('=')
                    k = export_cmd.sub('',k)
                    if not space_char.findall(k):
                        v = end_line.sub('',v)
                        if not space_char.findall(v):
                            var_dict[k] = v

    return var_dict

