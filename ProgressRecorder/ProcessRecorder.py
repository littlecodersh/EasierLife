import sys, json

class ProcessRecorder:
    def __enter__(self):
        return self
    def __init__(self, processName = 'DefaultProcess', localDataSet = {}, begin = None, total = None, warningMessage = '', jsonDir = ''):
        self.processName = processName
        self.localDataSet = localDataSet
        self.warningMessage = warningMessage
        self.jsonDir = jsonDir
        self.count = begin
        self.total = total
        self.process = -1
        self.jsonStorage = {}
        self.load_process()
    def load_process(self):
        try:
            with open('%sProcessRecorder.json'%self.jsonDir) as f: self.jsonStorage = json.loads(f.read())
            process_data = self.jsonStorage[self.processName]
            # only dictate above may move to except
            for key in self.localDataSet: 
                if process_data.has_key(key): self.localDataSet[key] = process_data[key]
            if self.count is None: self.count = process_data['__count']
            if self.total is None: self.total = process_data['__total']
        except:
            if self.count is None: self.count = 0
            if self.total is None: self.total = 100
    def store_process(self):
        if self.jsonStorage.has_key(self.processName):
            for key, value in self.localDataSet.items(): self.jsonStorage[self.processName][key] = self.localDataSet[key]
        else:
            self.jsonStorage[self.processName] = self.localDataSet
        self.jsonStorage[self.processName]['__count'] = self.count
        self.jsonStorage[self.processName]['__total'] = self.total
        with open('%sProcessRecorder.json'%self.jsonDir, 'w') as f: f.write(json.dumps(self.jsonStorage))
    def clear_storage(self):
        tmp_json = self.jsonStorage
        del tmp_json[self.processName]
        with open('%sProcessRecorder.json'%self.jsonDir, 'w') as f: f.write(json.dumps(tmp_json))
    def add(self, i = 1):
        self.count += i
        if self.process < self.count * 100 / self.total:
            self.process = self.count * 100 / self.total
            sys.stdout.write('%s: %s%s\r'%(self.warningMessage, self.process, '%'))
            sys.stdout.flush()
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.store_process()

if __name__ == '__main__':
    import time
    with ProcessRecorder(localDataSet = {'name':None, 'num':None, 'price':1}, warningMessage = 'First recorder') as pr:
        for key, value in pr.localDataSet.items(): print '%s: %s'%(key, value)
        for i in range(30):
            pr.add()
            time.sleep(0.05)
        pr.localDataSet['name'] = 'LittleCoder'
        pr.localDataSet['num'] = 1
        pr.localDataSet['price'] = '$1.99'
    print 'Pretent the program is closed and we start a new one'
    with ProcessRecorder(localDataSet = {'name':None, 'num':None, 'price':None}, warningMessage = 'First recorder') as pr:
        for key, value in pr.localDataSet.items(): print '%s: %s'%(key, value)
        for i in range(30):
            pr.add()
            time.sleep(0.05)
