import os, re
from os import listdir
from os.path import isfile, join

def get_heading(section):
    if section == 'input.tex':
        return '##Input##'
    elif section == 'output.tex':
        return '##Output##'
    elif section == 'scoring.tex':
        return '##Giới hạn:##'
    elif section == 'notes.tex':
        return '##Giải thích:##'
    else:
        return ''

def make_statement():
    path = join('package', 'statement-sections', 'vietnamese')
    files = [f for f in listdir(path) if isfile(join(path, f))]
    sections = ['legend.tex', 'input.tex', 'output.tex', 'example' ,'notes.tex', 'scoring.tex']
    s = bytes()
    line = "\n\n".encode('utf-8')

    for section in sections:
        if section == 'example':
            s += '##Ví dụ:##'.encode('utf-8')
            s += line
            example_files = [f for f in files if f.startswith('example')]
            for exp in example_files:
                index = int(exp.split('.')[1])
                if exp[-1] == 'a':
                    s += ('**Output ' + str(index) + ':**').encode('utf-8')
                else:
                    s += ('**Input ' + str(index) + ':**').encode('utf-8')
                s += line

                with open(join(path, exp), 'rb') as exp_text:
                    a = exp_text.read().split(b'\n')
                    for i in a:
                        s += b'    ' + i + b'\n'

        elif (isfile(join(path, section))):
            with open(join(path, section), 'rb') as infile:
                heading = get_heading(section)
                if heading:
                    s += heading.encode('utf-8')
                    s += line
                s += infile.read()
                s += line

    s = s.replace(b'$', b'~')
    s = s.replace(b'\\begin{itemize}', b'')
    s = s.replace(b'\\item', b'-')
    s = s.replace(b'\\end{itemize}', b'')
    s = re.sub(b"\\\\bf{(.*)}", b'**\\1**\n', s) 
    s = re.sub(b"\\\\it{(.*)}", b'*\\1*', s)
    s = s.replace(b'    -', b'-')

    with open(join('output', 'statement-lqdoj.txt'), 'wb') as f:
        f.write(s)



