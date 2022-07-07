import os, re
from os import listdir
from os.path import isfile, join

def get_heading(section):
    if section == 'input.tex':
        return '##Input'
    elif section == 'interaction.tex':
        return '##Tương tác'
    elif section == 'output.tex':
        return '##Output'
    elif section == 'scoring.tex':
        return '##Giới hạn:'
    elif section == 'notes.tex':
        return '##Giải thích:'
    else:
        return ''

def my_replace(st, l,r, new):
    #erase [l,r) range and replace with 'new'
    return st[:l] + new + st[r:]

def make_statement():
    path = join('package', 'statement-sections', 'vietnamese')
    files = [f for f in listdir(path) if isfile(join(path, f))]
    sections = ['legend.tex', 'input.tex', 'interaction.tex', 'output.tex', 'example' ,'notes.tex', 'scoring.tex']
    #s = bytes()
    s = str()
    endl = "\n\n"#.encode('utf-8')

    for section in sections:
        if section == 'example':
            s += '##Ví dụ:'#.encode('utf-8')
            s += endl
            example_files = [f for f in files if f.startswith('example')]
            for exp in example_files:
                index = int(exp.split('.')[1])
                if exp[-1] == 'a':
                    s += ('**Output ' + str(index) + ':**')#.encode('utf-8')
                else:
                    s += ('**Input ' + str(index) + ':**')#.encode('utf-8')
                s += endl

                with open(join(path, exp), 'r') as exp_text:
                    a = exp_text.read().split('\n')
                    for i in a:
                        s += '    ' + i + '\n'

        elif (isfile(join(path, section))):
            with open(join(path, section), 'r', encoding = 'utf-8') as infile:
                heading = get_heading(section)
                if heading:
                    s += heading#.encode('utf-8')
                    s += endl
                s += infile.read()
                s += endl

    specials = r"\`*_{}[]<>#+-.!|"

    s = s.replace(r'$', r'~')
    s = s.replace(r'~~', r'$$') #$$ is valid in both
    s = s.replace(r'\begin{center}', r'<center>')
    s = s.replace(r'\end{center}', r'</center>')

    # lists, nests supported
    # I do expect the .tex file to be well-formatted (endl by endl)
    
    indent = -4
    modes = [] # 0 : unordered, 1 : ordered 

    lines = str(s).split('\n')
    new_lines = []
    for line in lines:
        if line.count(r'\begin{itemize}'):
            indent += 4
            modes.append(0)
            line = line.replace(r'\begin{itemize}', '')
            print("Found unordered list")
        if line.count(r'\begin{enumerate}'):
            indent += 4
            modes.append(1)
            line = line.replace(r'\begin{enumerate}', '')
            print("Found ordered list")
        if line.count(r'\end{enumerate}') or line.count(r'\end{itemize}'):
            indent -= 4
            modes.pop(-1)
            line = line.replace(r'\end{enumerate}', '')
            line = line.replace(r'\end{itemize}', '')
            print("End list")
        if modes:
            mode = modes[-1]
            if mode == 0 :
                line = line.replace(r'\item', '-')
            else :
                line = line.replace(r'\item', '1.')
            line = " " * indent + line
        new_lines.append(line)

    s = "\n".join(new_lines)
    
    #simple text formats: bold font, italic, monospace, underline, struck out
    #and stupid quotes
    
    formats = [r'\bf{', r'\textbf{',
               r'\it{', r'\textit{',
               r'\t{', r'\tt{', 'r\texttt{',
               r'\sout{', r'\textsc{',
               r'`', r'``',
               r"'", r'}' #closing chars
               ]
    # r'\\emph{', r'\\underline{', impossible to do underline in markdown
               
    repls = [r'**', r'**',
             r'*', r'*',
             r'`', r'`', r'`',
             r'~~', r'~~',
             r"'", r'"'
             ]
    indexes = [0, 2, 4, 7, 9, 11]

    cur = 0
    INF = 10**9
    length = len(formats)
    positions = [None] * length
    modes = [] # reused, 0 : bold, 1 : italic, 2 : mono, 3 : strike, 4 : quote

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

        print("I found %s" % formats[opt])
        if opt < length - 2:
            #I only care about ", as the closing ' already correct
            if opt != 11:
                for i in range(len(indexes)-1,-1,-1):
                    if opt >= indexes[i]:
                        modes.append(i)
                        break
            s = my_replace(s, p, p+len(formats[opt]), repls[opt])
        else:
            md = modes[-1]
            if md < 4:
                s = my_replace(s, p, p+len(formats[opt]), repls[indexes[md]])
            else :
                s = my_replace(s, p, p+2, '"')
            modes.pop(-1)
        cur = p + 1
    
    # does this (below) really needed?
    # s = s.replace(b'    -', b'-')

    #code blocks
    s = s.replace(r'\begin{lstlisting}', r'```')
    s = s.replace(r'\end{lstlisting}', r'```')

    #polygon's stupid stuffs
    
    #confuses with html tags
    s = s.replace(r'<<', r'\<\<')
    s = s.replace(r'>>', r'\>\>') 
    #stupid!
    s = s.replace(r'~---', r'$&ndash;$')
    s = s.replace(r'"---', r'$&ndash;$')
    
    assert(type(s) == str)

    with open(join('output', 'statement-lqdoj.txt'), 'w', encoding = 'utf-8') as f:
        f.write(s)

# print("nice hehe")
# to-do list
# - text size
# - \url, \href
# - \includegraphics
# too sleepy rn

