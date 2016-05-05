#coding=utf8
import sys

def get_id_num():
    districtDict = {}
    with open('district.cfg') as f:
        for i in f: districtDict[i[6:].strip().decode('utf8')] = i[:6]
    def warn(fn):
        def _warn(*arg, **kwargs):
            r = fn(*arg, **kwargs)
            if r is None: raise Exception('Wrong %s!'%fn.__name__)
            return r
        return _warn
    @warn
    def district(name): return districtDict.get(name)
    @warn
    def date(date):
        try:
            return date if 10000000 <= int(date) <= 99999999 else None
        except:
            return
    @warn
    def uni_num(num):
        try:
            return '%03d'%int(num) if 0 <= int(num) <= 999 else None
        except:
            return
    def parity(s):
        n = '7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2'.split(' ')
        r = 0
        for i, j in zip(n, [c for c in s]): r += int(i) * int(j)
        return '1 0 X 9 8 7 6 5 4 3 2'.split(' ')[r%11]
    def _get_id_num(s): return s + parity(s)
    try:
        return _get_id_num(district(raw_input(u'District: [] ').decode(sys.stdin.encoding)) +
            date(raw_input(u'Date: [19220101] ')) +
            uni_num(raw_input(u'Code: [000] ')))
    except Exception, e:
        print(e)

if __name__ == '__main__':
    print(get_id_num())
