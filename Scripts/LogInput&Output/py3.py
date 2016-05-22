import sys

class outPip(object):
    def __init__(self, fileDir):
        self.fileDir = fileDir
        self.console = sys.stdout
    def write(self, s):
        self.console.write(s)
        with open(self.fileDir, 'a') as f: f.write(s)
    def flush(self):
        self.console.flush()

new_input = input
def inPip(fileDir):
    def _input(hint):
        s = new_input(hint)
        with open(fileDir, 'a') as f: f.write(s)
        return s
    return _input

sys.stdout = outPip('out.log')
input = inPip('out.log')

print('This will appear on your console and your file.')
print('So is this line.')
input('yo')
