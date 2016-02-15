import sys, traceback

from MailClient import MailClient
from MailProducer import MailProducer
from ExcelClient import ExcelClient

if __name__ == '__main__':
    mp = MailProducer()
    ec = ExcelClient(outputDir = 'run.xls', outputHeader =
            ['toName', 'toAddress', 'fromName', 'fromAddress', 'attachment', 'time', 'subject'])
    with MailClient() as mc:
        errorCount = 0
        while 1:
            mailData = mc.get_mail()
            if mailData is None: break
            try:
                mailData = mp.mail_produce(mailData)
                ec.storeData([mailData['toName'], mailData['toAddress'], mailData['fromName'],
                    mailData['fromAddress'], mailData['attachment'], mailData['time'], mailData['subject']])
                sys.stdout.flush()
                sys.stdout.write('Finished: %s %s\r'%(mc.process, '%'))
            except:
                with open('mail.txt%s'%errorCount, 'w') as f: f.write(mailData)
                errorCount += 1
                traceback.print_exc()
