#MysqlClient 160223
    Aimed at:
        Save time when dealing with MySQL and make it easy to get data one by one
    Environment:
        Windows 8.1 - 64
        Python 2.7.10 (MySQLdb installed: https://pypi.python.org/pypi/MySQL-python/1.2.5）
    Attention:
        paralled input and fetch is in paralled_get_source_of_data_source function
        get function which is used to get data one by one from data_source function
        MAX_NUM can be changed based on local calculating speed and time consuming of data processing

    目标：
        节省MySQL相关操作的时间以及实现逐条读出MySQL中的数据
    环境：
        Windows 8.1 - 64
        Python 2.7.10 （安装MySQLdb: https://pypi.python.org/pypi/MySQL-python/1.2.5）
    注意事项：
        并行读取与输出的操作在paralled_get_source_of_data_source中
        通过data_source方法获取用于逐个取出数据的方法
        MAX_NUM的量可以通过本机速度与数据处理语句的多少自行修改
