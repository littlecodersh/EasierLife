import MySQLdb, re, thread

DEFAULT_CONFIG = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': 'root', 'db': 'witcampus', 'charset': 'utf8'}
MAX_NUM = int(1e6)

def source_function(fn, *args, **kwargs): # get a iter item fn and return a function to get data one at a time
    def wrapped(*args, **kwargs):
        s = fn(*args, **kwargs)
        def return_item():
            try:
                return s.next()
            except StopIteration:
                return None
        return return_item
    return wrapped
def get_data_from_source(r): # get a function returns a data one at a time and a funtion deals with it, get everything done
    def source(fn, *args, **kwargs):
        def wrapped(*args, **kwargs):
            while 1:
                data = r()
                if data is None: break
                fn(data, *args, **kwargs)
        return wrapped
    return source

class MysqlClient:
    def __init__(self, **config):
        if not config: config = DEFAULT_CONFIG
        self._connection = MySQLdb.connect(**config)
        self._cursor = self._connection.cursor()
        self._storedDataSource = None
    def query(self, sql):
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    @source_function
    def simple_data_source(self, sql): # return a function to provide one data at a time
        c = self._connection.cursor()
        c.execute(sql)
        for item in c.fetchall(): yield item
    @source_function
    def parallel_get_source_of_data_source(self, sql):
        regex = re.compile('from (\S+)')
        tableName = re.findall(regex, sql)[0]
        totalNum = self.query('select count(*) from %s'%tableName)[0][0]
        unitNumber = int(totalNum / MAX_NUM)
        def get(i):
            self._storedDataSource = self.simple_data_source('%s limit %s, %s'%(sql, i * MAX_NUM, MAX_NUM if i != unitNumber else totalNum - i * MAX_NUM))
        get(0)
        if unitNumber == 0: yield self._storedDataSource
        for i in range(1, unitNumber + 2):
            while self._storedDataSource is None: print 'Thread sucks'
            r = self._storedDataSource
            self._storedDataSource = None
            thread.start_new_thread(get, (i,))
            yield r
    @source_function
    def data_source(self, sql): # limit is now useless here
        sourceOfDataSource = self.parallel_get_source_of_data_source(sql)
        # I failed to use get_data_from_source here and don't know why
        while 1:
            dataSource = sourceOfDataSource()
            if dataSource is None: break
            while 1:
                data = dataSource()
                if data is None: break
                yield data

if __name__ == '__main__':
    mc = MysqlClient()

    r = mc.data_source('select * from dev_loc order by node_id')
    @get_data_from_source(r)
    def p(data): print str(data)
    p()
