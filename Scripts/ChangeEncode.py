import os

for t in os.walk('.'):
    for _file in t[2]:
        if(_file[-2:] == '.h' or _file[-4:] == '.cpp'):
            print('%s is processing'%_file)
            with open(_file) as f:
                with open(os.path.join('encoding', _file), 'w') as output:
                    output.write(f.read().decode('utf8').encode('cp936'))
