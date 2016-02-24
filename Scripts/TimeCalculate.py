import time

def TimeCalculate(fn, *args, **kwargs):
    def wrapped(*args, **kwargs):
        beginTime = time.time()
        result = fn(*args, **kwargs)
        return (time.time() - beginTime, result)
    return wrapped

if __name__ == '__main__':
    @TimeCalculate
    def fn():
        for i in range(int(1e7)):
            pass
    print fn()

