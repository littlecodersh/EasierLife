import MySQLdb, re, thread
import json, sys

DEFAULT_CONFIG = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': 'root', 'db': 'witcampus', 'charset': 'utf8'}
MAX_NUM = int(1e5)

class MysqlClient:
    def __init__(self, **config):
        if not config: config = DEFAULT_CONFIG
        self._connection = MySQLdb.connect(**config)
        self._cursor = self._connection.cursor()
        self._storedDataSource = None
        self._cursor.execute('set sql_notes = 0') # disable warnings
    def set_emergency_mode():
        self._cursor.execute('set global max_allowed_packet = 1024M')
        self._cursor.execute('set global wait_timeout = 600')
    def query(self, sql):
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    def insert_data(self, tableName, items = []):
        items = ['"%s"'%item for item in items]
        self._cursor.execute('insert into %s values(%s)'%(tableName,', '.join(items)))
        self._connection.commit()
    def restruct_table(self, tableName, orderBy, restructedTableName = None):
        if restructedTableName is None: restructedTableName = 'restructed_' + tableName
        orderByString = ', '.join(['%s %s'%(key[0], key[1]) for key in orderBy])
        self.query(self.query('show create table %s'%tableName)[0][1].replace(tableName, restructedTableName, 1))
        sys.stdout.write('Restructuring the data storage...\r')
        totalNum = self.query('select count(*) from %s'%tableName)[0][0]
        s = self.data_source('select * from %s order by %s'%(tableName, orderByString))
        count = 0
        totalCount = 0
        process = -1
        for data in s:
            insertSql = 'insert into %s values (%s)'%(restructedTableName, ', '.join(['%s' for i in range(len(data))]))
            self._cursor.execute(insertSql, data)
            count += 1
            totalCount += 1
            if process < totalCount * 100 / totalNum:
                process = totalCount * 100 / totalNum
                sys.stdout.flush()
                sys.stdout.write('Restructuring the data storage: %s%s\r'%(process, '%'))
            if count >= MAX_NUM:
                count = 0
                self._connection.commit()
        self._connection.commit()
        print 'Restructuring Finished'
        return restructedTableName
    def simple_data_source(self, sql): # return a function to provide one data at a time
        c = self._connection.cursor()
        c.execute(sql)
        for item in c.fetchall(): yield item
    def parallel_get_source_of_data_source(self, sql, beginNumber = 0):
        regex = re.compile('from (\S+)')
        tableName = re.findall(regex, sql)[0]
        totalNum = self.query('select count(*) from %s'%tableName)[0][0]
        unitNumber = totalNum / MAX_NUM + 1
        self._storedDataSource = self.simple_data_source('%s limit %s, %s'%(sql, beginNumber, MAX_NUM))
        def get(i):
            self._storedDataSource = self.simple_data_source('%s limit %s, %s'%(sql, i * MAX_NUM, MAX_NUM))
        if unitNumber == beginNumber / MAX_NUM: yield self._storedDataSource
        for i in range(beginNumber / MAX_NUM + 1, unitNumber + 1):
            while self._storedDataSource is None: print 'Thread sucks'
            r = self._storedDataSource
            self._storedDataSource = None
            thread.start_new_thread(get, (i,))
            yield r
    def data_source(self, sql): # limit is now useless here
        regex = re.compile('(select .*? from .*?)(?: limit (\S+),.*)?$')
        r = re.findall(regex, sql)[0]
        sourceOfDataSource = self.parallel_get_source_of_data_source(r[0], int(r[1]) if r[1] else 0)
        for dataSource in sourceOfDataSource:
            for data in dataSource: yield data

if __name__ == '__main__':
    mc = MysqlClient()
    mc.restruct_table('device', [('dev_id',''), ('node_des','desc')])

    # a = {'a':'1',}
    # import datetime
    # mc.insert_data('acrecenv', ['json', datetime.datetime.now(), MySQLdb.escape_string(json.dumps(a))])

    # r = mc.data_source('select * from dev_loc order by node_id limit 300, 100')
    # for item in r: print item
