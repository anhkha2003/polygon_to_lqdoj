from zipfile import ZipFile
import subprocess
import os 
from os import listdir
from os.path import isfile, join
import shutil

tests_path = join('package', 'tests')

# unzip file tests
def unzip_package(name):
    try: 
        shutil.rmtree('package')
    except Exception:
        pass
    with ZipFile(name + '.zip', 'r') as zip_ref:
        zip_ref.extractall('package')

# run doall.bat
def run_doall():
    os.chdir('package')
    if isfile("doall.bat"):
        subprocess.call([r"doall.bat"])
    os.chdir('..')

# rename files input/output
def rename_files():
    files = [f for f in listdir(tests_path) if isfile(join(tests_path, f))]
    for f in files:
        if '.' in f: 
            name = f.split('.')[0]
            new_name = name + '.out'
        else:
            new_name = f + '.inp'
        os.rename(join(tests_path, f), join(tests_path, new_name))

# zip file tests
def zip_tests():
    files = [f for f in listdir(tests_path) if isfile(join(tests_path, f))]
    with ZipFile(join('output', 'tests.zip'), 'w') as zipf:
        for f in files:
            zipf.write(join(tests_path, f), f)


