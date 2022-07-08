from process_tests import *
from process_statement import *

with open('name.txt', 'r') as f:
    NAME = f.read()
    
try: 
    os.mkdir('output')
except Exception:
    pass
 
unzip_package(NAME)
path = join('package', 'statements', 'vietnamese')
os.makedirs(path, exist_ok=True)
shutil.copy(join('package', NAME + '.tex'), join(path, 'problem.tex'))
make_statement()