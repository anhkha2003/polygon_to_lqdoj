#References:
#https://polygon.codeforces.com/docs/statements-tex-manual
#https://www.markdownguide.org/cheat-sheet/
#lqdoj.edu.vn / admin interface

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
    #escape specials

    s = s.replace(r'$', r'~')
    s = s.replace(r'~~', r'$$') #$$ is valid in both
    s = s.replace(r'\begin{center}', r'<center>')
    s = s.replace(r'\end{center}', r'</center>')

    #code blocks
    unique = r'.]]'
    s = s.replace(r'\begin{lstlisting}', unique)
    s = s.replace(r'\end{lstlisting}', unique)

    #links
    links_count = 0
    while True :
        pos = s.find(r'\url{')
        if pos == -1:
            break
        nxt = s.find(r'}', pos)
        assert(nxt != -1)
        link = s[pos+len(r'\url{') : nxt]
        links_count += 1
        if links_count == 1:
            s += endl
        s = my_replace(s, pos, nxt+1, '[%s][%d]' % (link, links_count))
        s += '  [%d]: %s\n' % (links_count, link)
        
    while True :
        pos = s.find(r'\href{')
        if pos == -1:
            break
        nxt = s.find(r'}', pos)
        assert(nxt != -1)
        link = s[pos+len(r'\href{') : nxt]
        
        assert(s[nxt+1] == '{')
        final = s.find(r'}', nxt+1)
        caption = s[nxt+2:final]
        
        links_count += 1
        if links_count == 1:
            s += endl
        s = my_replace(s, pos, final+1, '[%s][%d]' % (caption, links_count))
        s += '  [%d]: %s\n' % (links_count, link)

    print("Done links, there were %d" % links_count)
        
    # lists, nests supported
    # I do expect the .tex file to be well-formatted (line by line)
    
    indent = -2
    modes = [] # 0 : unordered, 1 : ordered 

    lines = str(s).split('\n')
    new_lines = []
    for line in lines:
        if line.count(r'\begin{itemize}'):
            indent += 2
            modes.append(0)
            line = line.replace(r'\begin{itemize}', '')
            print("Found unordered list")
        if line.count(r'\begin{enumerate}'):
            indent += 2
            modes.append(1)
            line = line.replace(r'\begin{enumerate}', '')
            print("Found ordered list")
        if line.count(r'\end{enumerate}') or line.count(r'\end{itemize}'):
            indent -= 2
            modes.pop(-1)
            line = line.replace(r'\end{enumerate}', '')
            line = line.replace(r'\end{itemize}', '')
            print("End list")
        if modes:
            mode = modes[-1]
            line = line.strip()
            if mode == 0 :
                line = line.replace(r'\item', '-')
            else :
                line = line.replace(r'\item', '1.')
            line = " " * indent + line
        new_lines.append(line)

    s = "\n".join(new_lines)

    #text sizes (headings), not support \tiny, \scriptsize, \small, \normalsize
    #cant be nested with any other elements

    formats = [r'\large{',
               r'\Large{',
               r'\LARGE{',
               r'\huge{',
               r'\Huge{',
               r'\tiny{', r'\scriptsize{', r'\small{', r'\normalsize{'
               r'}']
               
    repls = [r'<h5>',
             r'<h4>',
             r'<h3>',
             r'<h2>',
             r'<h1>',
             '']

    for i in range(len(formats)):
        cur = 0
        while True:
            cur = s.find(formats[i], cur)
            if cur == -1:
                break
            print("I found %s" % formats[i])
            s = my_replace(s, cur, cur+len(formats[i]), repls[min(i, len(repls)-1)])
            cur = s.find(r'}', cur)
            new = str()
            if i < 5:
                new = repls[i]
                new = my_replace(new, 1,1, '/')
            s = my_replace(s, cur, cur+1, new)
    print("Done headings")

    #simple text formats: bold font, italic, monospace, underline, struck out
    #and stupid quotes, and super tricky exceptions in math & code
    
    formats = [r'\bf{', r'\textbf{',
               r'\it{', r'\textit{',
               r'\t{', r'\tt{', r'\texttt{',
               r'\sout{', 
               r'``',
               r'`',
               r'~', r'$$', #maths
               unique, #for code 
               r'\emph{', r'\underline{', r'\textsc{',
               #note: impossible to do underline in markdown && textsc is CAP
               r"'", r'}', #close characters
               ]
               
    repls = [r'**',
             r'*',
             r'`',
             r'~~',
             r'"',
             r"'",
             '', '', ''
             ]
    indexes = [0, 2, 4, 7, 8, 9, 10, 12, 13, 16]

    is_math = False
    is_code = False
    cur = 0
    INF = 10**9
    length = len(formats)
    positions = [None] * length
    modes = []
    # 0: bold, 1: italic, 2: mono, 3: strike, 4,5: quote,
    # 6: math, 7: code, 8: ignore, 9: close

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

        new = str()
        print("I found %s" % formats[opt])
        if opt < indexes[9]:
            for i in range(len(indexes)-1,-1,-1):
                if opt >= indexes[i]:
                    if i == 6:
                        is_math = not is_math
                        cur = p + len(formats[opt])
                    elif i == 7:
                        is_code = not is_code
                        cur = p + len(formats[opt])
                    else:
                        modes.append(i)
                        s = my_replace(s, p, p+len(formats[opt]), repls[i])
                        cur = p + len(repls[i])
                    break
        else:
            if formats[opt] == r'}' and is_math:
                cur = p+1
                continue
            if not modes:
                cur = p+1
                continue #can catch wild }?
            md = modes[-1]
            assert(md != 6 and md != 7 and md < 9)
            s = my_replace(s, p, p+len(formats[opt]), repls[md])
            modes.pop(-1)
            cur = p + len(repls[md])

    print("Done text formattings")

    #adjust
    s = s.replace(unique, r'```')
    
    #polygon's stupid stuffs
    
    #confuses with html tags
    #note: allow <,> in math & code
    #s = s.replace(r'<<', r'\<\<')
    #s = s.replace(r'>>', r'\>\>')
    #confuses with C++ I/O
    #solution: skip
    
    #stupid!
    s = s.replace(r'~---', r'~&ndash;~')
    s = s.replace(r'"---', r'~&ndash;~')
  
    with open(join('output', 'statement-lqdoj.txt'), 'w', encoding = 'utf-8') as f:
        f.write(s)

# tabulars and images