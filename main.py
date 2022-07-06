from process_tests import *
from process_statement import *

with open('name.txt', 'r') as f:
    NAME = f.read()
    
try: 
    os.mkdir('output')
except Exception:
    pass

unzip_package(NAME)
run_doall()
rename_files()
zip_tests()
make_statement()