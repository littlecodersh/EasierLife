import datetime

TEMPLATE_CONTENT_DIR = 'content.enex'
TEMPLATE_HEADER_DIR = 'header.enex'
FIRST_MONDAY_DATE = datetime.datetime(2016, 1, 4)

class Memo:
    def __init__(self):
        self.memoData=[]
        self.now = datetime.datetime.now()
        self.dataList = {}
        self.load_memo_template()
        self.load_time()
        self.update_template()
    def load_memo_template(self):
        with open(TEMPLATE_CONTENT_DIR) as f: self.memoData.append(f.read())
        with open(TEMPLATE_HEADER_DIR) as f: self.memoData.append(f.read())
    def load_time(self):
        self.dataList['month'] = self.now.strftime('%B')
        # if it's weekends, this will produce next week's memo
        if self.now.weekday() > 4:
            self.now += datetime.timedelta(days = 7 - self.now.weekday())
        else:
            self.now -= datetime.timedelta(days = self.now.weekday())
        self.dataList['day'] = self.now.strftime('%d')
        # self.dataList['week'] = str((self.now - FIRST_MONDAY_DATE).days / 7 + 1)
        self.dataList['week'] = self.now.strftime('%U')
        for i in range(7): 
            self.dataList[str(i)] = (self.now + datetime.timedelta(days = i) - datetime.timedelta(self.now.weekday())).strftime('%y%m%d')
    def update_template(self):
        for key, value in self.dataList.items():
            for i in range(2):
                self.memoData[i] = self.memoData[i].replace('[^'+key+']',value)
        print 'Memo Created!'
        print 'Week: %s' %(self.dataList['week'])
        print 'Day : %s - %s' %(self.dataList['0'],self.dataList['6'])
    def output_memo(self):
        return self.memoData[1].replace('[^content]',self.memoData[0])
    def raw_memo(self):
        return self.memoData[0]

if __name__ == '__main__':
    m = Memo()
    with open('OUTPUT.enex', 'w') as o:
        o.write(m.output_memo())
