import sys, time

class ProgressBar:
    def __enter__(self):
        return self
    def __init__(self, count=0, total=100, width=50):
        self.count=count
        self.total=total
        self.width=width
    def move(self, i=1):
        self.count+=i
        return True
    def move_to(self,count):
        self.count=count
    def log(self,s=''):
        if self.count > self.total: 
            print
            raise Exception('Task Done!')
        sys.stdout.write(' '*(self.width+9)+'\r')
        sys.stdout.flush()
        if s != '': print s
        progress = self.width * self.count / self.total
        sys.stdout.write('{0:3}/{1:3}:'.format(self.count, self.total))
        sys.stdout.write('|'*progress + '-'*(self.width - progress) + '\r')
        sys.stdout.flush()
    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

if __name__ == '__main__':
    with ProgressBar(0,50,50) as p:
        try:
            i = 0
            while p.move():
                i+=1
                p.log('This is: ' + str(i))
                time.sleep(.1)
        except Exception, e:
            print e
