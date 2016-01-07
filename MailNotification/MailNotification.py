#coding=utf8
import smtplib, json, time
from email.mime.text import MIMEText

RECEIVE_ACCOUNT = '2807342354@qq.com'

class MailNotification():
    def __init__(self):
        pass
    def __enter__(self):
        self.receiveAccount = RECEIVE_ACCOUNT
        self.get_account()
        self.connect_host()
        return self
    def get_account(self):
        with open('config.json') as f:
            config = json.loads(f.read())
            self.account = config['account']
            self.password = config['password']
            self.host = config['host']
            self.postfix = config['postfix']
    def connect_host(self):
        self.server = smtplib.SMTP()
        self.server.connect(self.host)
        self.server.ehlo()  
        self.server.starttls()  
        self.server.ehlo()  
        self.server.set_debuglevel(1)
        self.server.login(self.account, self.password)
    def send_text(self, from_, to_, subject, text, text_type):
        msg = MIMEText(text.encode('utf-8'), _subtype=text_type, _charset='utf-8')
        msg['Subject'] = subject.encode('utf-8')
        me = '<' + from_ + '>'
        msg['From'] = me
        msg['To'] = ';'.join(to_)
        self.server.sendmail(from_, to_, msg.as_string())
    def send_notification(self, notification):
        self.send_text(self.account + self.postfix, [self.receiveAccount],
                'Notification From Client',
                notification + '\n' + time.ctime(),
                'plain')
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.server.close()

if __name__=='__main__':
    with MailNotification() as mail:
        mail.send_notification('First mail notification!')
