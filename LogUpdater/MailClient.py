#coding=utf8
import poplib, json
from email import parser  
  
class MailClient:
    def __init__(self):
        pass
    def __enter__(self):
        self.load_config()
        self.login()
        self.totalProcess = len(self.client.list()[1]) + 1
        self.mailSource = self.get_mail_source()
        self.process = 0
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.client.quit()
    def load_config(self):
        with open('config.json') as f: config = json.loads(f.read())
        self.userID = '%s@%s'%(config['userID'], config['postfix'])
        self.password = config['password']
        self.host = config['host']
    def login(self):
        self.client = poplib.POP3_SSL(self.host)  
        self.client.user(self.userID)  
        self.client.pass_(self.password)  
        print 'Login successfully'
    def get_mail_source(self):
        for i in range(1, self.totalProcess):
            self.process = int(i * 100 / self.totalProcess)
            yield str(parser.Parser().parsestr('\n'.join(self.client.retr(i)[1])))
    def get_mail(self):
        try:
            return self.mailSource.next()
        except StopIteration:
            return None

if __name__ == '__main__':
    with MailClient() as mc:
        with open('mail.txt','w') as f: f.write(mc.get_mail())
