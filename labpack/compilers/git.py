__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

'''
PLEASE NOTE:    git package requires the git command line tool.

(all platforms) sudo apt-get install git
'''


import re
import subprocess
from os import devnull

try:
    subprocess.Popen(["git", "--version"], stdout=subprocess.PIPE)
except:
    import sys
    print('git package requires the git command line tool. try: sudo apt-get install git')
    sys.exit(1)

def merge_diff(target, source, output=''):
   
    '''
        a method to merge the non-conflicting diffs between two files
        
        method retrieves the results from `git diff --no-index target source`
        and adds to target the lines from additions found in source. diff
        results which would subtract lines from target are ignored.
        
        PLEASE NOTE:    method makes no check to ensure that target, source
                        or output are valid paths
                        
    :param target: string with path to file for target data
    :param source: string with path to file for source data
    :param output: [optional] string with path to file to save output of merge
    :return: string with merged diff data
    '''
    
    # run git diff
    cmd = 'git --no-pager diff --no-index %s %s' % (target, source)
    out = subprocess.run(cmd.split(' '), stderr=open(devnull, 'wb'), stdout=subprocess.PIPE)
    diff = out.stdout.decode("utf-8")

    # retrieve target text
    text = open(target).read()
    if not diff:
        return text

    # remove header from diff
    head = re.compile('^(.*? @@\n)', re.S)
    diff = head.sub('', diff).strip()

    # iterate over remaining diff
    merged = ''
    chunk = []
    lines = diff.split('\n')
    while lines:
        line = lines.pop(0)
        # find additions
        if line[0] == '+':
            if chunk:
                # don't add line if chunk has conflict
                if chunk[-1][0] == '-':
                    continue

        elif line[0] == ' ':
            if chunk:
                # toss previous chunks with conflicts or subtractions
                if chunk[-1][0] == '-':
                    chunk = []
                # add new lines from chunks with only additions
                elif chunk[-1][0] == '+':
                    existing = ''
                    addition = ''
                    for l in chunk:
                        if l[0] == ' ':
                            existing += l[1:] + '\n'
                        else:
                            addition += l[1:] + '\n'
                    # find end of existing part of text and add to merged
                    if existing:
                        pattern = re.compile(re.escape(existing), re.S)
                        matches = pattern.finditer(text)
                        for match in matches:
                            index = match.end(0)
                            previous = text[:index]
                            merged += previous
                            # update text to current index
                            text = text[index:]
                            break
                    # add additional lines to merged and reset chunk
                    merged += addition
                    chunk = []

        # add line to chunk
        chunk.append(line)

    # add additions if at end of file
    if chunk:
        if chunk[-1][0] == '\\':
            if chunk[-1].find('No newline at end of file') > -1:
                exist = []
                add = []
                while chunk[-1][0] != ' ':
                    if chunk[-1][0] == '+':
                        add.insert(0, chunk.pop()[1:])
                    elif chunk[-1][0] == '-':
                        exist.insert(0, chunk.pop()[1:])
                    else:
                        chunk.pop()
                    if not chunk:
                        break
                if add:
                    for line in exist:
                        add.pop(0)
                        if not add:
                            break
                merged += text
                if add:
                    merged += '\n' + '\n'.join(add)
                text = ''

    # else add remaining text
    if text:
        merged += text

    # save to output
    if output:
        with open(output, 'wt') as f:
            f.write(merged)
            f.close()

    return merged