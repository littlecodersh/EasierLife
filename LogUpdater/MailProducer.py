#coding=utf8
import re

class MailProducer:
    def __init__(self):
        findPattern = ('发件人: (.*?)\n'
        + '发送时间: (.*?)\n'
        + '收件人: (.*?)\n'
        + '(?:抄送: .*?\n)?'
        + '主题: (.*?)\n').decode('utf8')
        matchPattern = findPattern.replace('(.*?)', '.*?')
        self.findRegex = re.compile(findPattern)
        self.matchRegex = re.compile(matchPattern)
    def mail_produce(self, mailData, mailUser):
        # will return a list of email
        # [[sender, time, receiver, topic, content],[]]
        r = []
        if len(mailUser) != 4: raise Exception('mailUser input error')
        mailInfo = self.findRegex.findall(mailData)
        mailInfo.insert(0, mailUser)
        mailContent = self.matchRegex.split(mailData)
        for i in range(len(mailInfo)):
            data = []
            for j in mailInfo[i]: data.append(j)
            data.append(mailContent[i])
            r.append(data)
        return r

if __name__ == '__main__':
    with open('email.txt') as f: text = f.read().decode('cp936')
    mp = MailProducer()
    mp.mail_produce(text, ['@@@','@@@','@@@','@@@'])
    for i in mp.mail_produce(text, ['@@@','@@@','@@@','@@@']):
        print i
        print 
