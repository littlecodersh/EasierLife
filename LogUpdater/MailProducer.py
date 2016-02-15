#coding=utf8
import re, base64, quopri

class MailProducer:
    def __init__(self):
        self.regexDic = {
                'time': '[(?:Received)(?:Date)]:[\s\S]*?([A-Za-z]{3}, \d{2} [A-Za-z]{3} \d{4} \d\d:\d\d:\d\d \+\d{4})',
                'from': 'From: (.*?)\n',
                'to': 'To: (.*?)\n',
                'subject': 'Subject: ([\s\S]*?)\n.*?[^\?=]{2}\n',
                'attachment': 'Content-Disposition: attachment;[\s\S]*?filename="([\s\S]*?)"',}
        for (key, regex) in self.regexDic.items():
            self.regexDic[key] = re.compile(regex)
    def mail_produce(self, mailData):
        r = {}
        for (key, regex) in self.regexDic.items():
            if key != 'attachment':
                match = re.search(regex, mailData)
                r[key] = match.group(1).replace('\n', '') if match else None
            else:
                match = re.findall(regex, mailData)
                r[key] = match
        if r['time']:
            regex = re.compile('[A-Za-z]{3}, (\d{2}) ([A-Za-z]{3}) (\d{4}) \d\d:\d\d:\d\d \+\d{4}')
            monthDic = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12',}
            match = re.search(regex, r['time'])
            r['time'] = '%s-%s-%s'%(match.group(3), monthDic[match.group(2)], match.group(1))
        if r['from']:
            regex = re.compile('^(.*) <(\S*)>$')
            match = re.search(regex, r['from'])
            if match:
                r['fromName'] = self.decode_string(match.group(1))
                r['fromAddress'] = match.group(2)
            else:
                r['fromName'] = ''
                r['fromAddress'] = r['from'][1:-1]
        if r['to']:
            regex = re.compile('^(.*) <(\S*)>$')
            match = re.search(regex, r['to'])
            if match:
                r['toName'] = self.decode_string(match.group(1))
                r['toAddress'] = match.group(2)
            else:
                r['toName'] = ''
                r['toAddress'] = r['to'][1:-1]
        if r['subject']:
            r['subject'] = self.decode_string(r['subject'])
        if r['attachment']:
            r['attachment'] = ', '.join([self.decode_string(atta) for atta in r['attachment']])
        else:
            r['attachment'] = ''
        return {key:value for key,value in r.items() if key in (
            'toName', 'toAddress', 'fromName', 'fromAddress', 'attachment', 'time', 'subject')}
    def decode_string(self, s):
        if not s: return ''
        while s[0] == ' ': s = s[1:]
        while s[-1] == ' ': s = s[:-1]
        if '\n' in s: return ''.join([self.decode_string(sps) for sps in s.split('\n')])
        if ' ' in s: return ''.join([self.decode_string(sps) for sps in s.split(' ')])
        regex = re.compile('^(.*?)=\?(.*?)\?(.*?)\?(.*?)\?=(.*?)$')
        match = re.search(regex, s)
        if match:
            if not match.group(3) in ('Q', 'B'): raise Exception('Unknown Encode: %s'%match.group(3))
            decodeFn = {'B': base64.b64decode, 'Q': quopri.decodestring,}
            r = '%s%s%s'%(match.group(1), decodeFn[match.group(3)](match.group(4)).decode(match.group(2)), match.group(5))
        else:
            r = s
        while r[0] == '"' or r[0] == '\'': r = r[1:]
        while r[-1] == '"' or r[-1] == '\'': r = r[:-1]
        return r

if __name__ == '__main__':
    with open('mail.txt') as f: text = f.read().decode('utf8')
    mp = MailProducer()
    for (i,j) in mp.mail_produce(text).items():
        print '%s: %s'%(i,j)
