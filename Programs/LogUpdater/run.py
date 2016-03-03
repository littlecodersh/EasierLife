from lib.producexml import producexml
from lib.makeuploadfile import makeuploadfile
from lib.uploadlog import uploadlog

print 'Hello Zhou, nice to see you again:)'
print 'How much work log have you earned this time?'
print 'Get tasks done one by one and log will be updated.'
print

def get_option():
    print 'Tasks List:'
    print '[1] Produce Xml File'
    print '[2] Make Up Upload File'
    print '[3] Upload Everything Prepared'
    while 1:
        r = raw_input('Task select: ')
        if r in ('1','2','3'): print;return r

taskDict = {'1':producexml, '2':makeuploadfile, '3':uploadlog}

if __name__ == '__main__':
    while 1:
        taskDict[get_option()]()
        print
        if raw_input('Quit?[q]') == 'q': break;
