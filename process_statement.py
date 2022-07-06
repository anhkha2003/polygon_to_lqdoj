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

def my_replace(st, l,r, new):
    #erase [l,r) range and replace with 'new'
    st = st[:l] + new + st[r:]

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

    specials = r"\`*_{}[]<>#+-.!|"

    s = s.replace(b'$', b'~')
    s = s.replace(b'~~', b'$$') #$$ is valid in both
    s = s.replace(b'\begin{center}', b'<center>')
    s = s.replace(b'\end{center}', b'</center>')

    # lists, nests supported
    # I do expect the .tex file to be well-formatted (line by line)
    
    indent = 0
    modes = [] # 0 : unordered, 1 : ordered 

    lines = str(s).split('\n')
    for line in lines:
        if line.count('\\begin{itemize}'):
            indent += 4
            modes.append(0)
        if line.count('\\begin{enumerate}'):
            indent += 4
            modes.append(1)
        if line.count('\\end{enumerate}') or line.count('\\end{itemize}'):
            indent -= 4
            modes.pop(-1)
        if modes:
            mode = modes[-1]
            if mode == 0 :
                line = line.replace('\\item', b'-')
            else :
                line = line.replace('\\item', b'1.')
            line = " "*indent + line

    s = "\n".join(lines)
    
    #simple text formats: bold font, italic, monospace, underline, struck out
    #and stupid quotes
    
    formats = ['\\bf{', '\\textbf{',
               '\\it{', '\\textit{',
               '\\t{', '\\tt{', '\\texttt{',
               # b'\\emph{', b'\\underline{', impossible to do underline in markdown
               '\sout{', '\textsc{',
               '`', '``'
               ]
    repls = ['**', '**',
             '*', '*',
             '`', '`', '`',
             '~~', '~~',
             "'", '"']   

    cur = 0
    INF = 10**9
    length = len(formats)
    positions = [None] * length

    while True :
        opt = 0
        for i in range(length):
            positions[i] = s.find(formats[i], cur)
            if positions[i] == -1 :
                positions[i] = INF
            if positions[i] < positions[opt] :
                opt = i
        p = positions[opt] 
        if p == INF :
            break

        my_replace(s, p, p+len(formats[opt]), repls[opt])
        cur = p + 1
        if opt < (2+2+3+2) :
            cur = s.find('}', cur)
        else :
            cur = s.find("'" * len(formats[opt]), cur)
        my_replace(s, cur, cur+1, repls[opt])

    
    # does this (below) really needed?
    # s = s.replace(b'    -', b'-')

    #code blocks
    s = s.replace('\\begin{lstlisting}', '```')
    s = s.replace('\\end{lstlisting}', '```')

    #polygon's stupid stuffs
    
    #confuses with html tags
    s = s.replace('<<', '\<\<')
    s = s.replace('>>', '\>\>') 
    #stupid!
    s = s.replace('~---', '$&ndash;$')
    s = s.replace('"---', '$&ndash;$')
    

    with open(join('output', 'statement-lqdoj.txt'), 'wb') as f:
        f.write(bytes(s, 'utf-8'))

# print("nice hehe")
# to-do list
# - text size
# - \url, \href
# - \includegraphics
# too sleepy rn

